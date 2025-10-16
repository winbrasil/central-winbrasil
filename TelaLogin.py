from bibliotecas import *
from TelaCadastramento import *


class TelaLogin(Screen):
    def __init__(self, **kwargs):
        #super().__init__(**kwargs)
        self.win = Window
        self.app = MDApp.get_running_app()
        
        self.fonte_padrao = self.app.fonte_padrao
        super().__init__(**kwargs)
        #self.app.root.get_screen("tela_cadastramento")
        
    def on_enter(self):
        cx_s = self.ids.cx_s

        for widget in self.ids.box_cxs.walk():
            if isinstance(widget, TextInput):
                if widget ==cx_s:
                    widget.text = ""
        
        
    def verificar_login(self, *args):
        try:
            self.db_api = MDApp.get_running_app().db_api
            cx_u = self.ids.cx_u
            cx_s = self.ids.cx_s
            cx_u_text = cx_u.text.strip()
            cx_s_text = cx_s.text.strip()
            
            cxs = [cx_u, cx_s]
            cxs_text = [ cx_s_text, cx_u_text]
            
            if not all(cxs_text):
                for cx in cxs:
                    if not cx.text.strip():
                        cx.line_color_normal =(1,0,0,1)
                    else:
                        cx.line_color_normal = (1,1,1,1)
                        
                self.app.gerenciamento_info_geral("[b](!)[/b] [color=#ffff00]Prencha todos os campos!")
                
                
            else:
                #self.app.on_start()
                resultado, msg= self.login_firebase(email=cx_u_text, senha=cx_s_text, verificado=True)
                
                if resultado:
                    Clock.schedule_once(lambda dt: setattr(self.app, "permissao_temporaria_login", True), 0)
                    Clock.schedule_once(lambda dt: setattr(self.app, "usuario_verificado", True), 0)
                    
                    self.app.gerenciamento_info_geral(f"[color=#ff0000]{msg}")
                    self.app.root.current = "tela_inicial"
                    
                else:
                    self.app.gerenciamento_info_geral(f"[color=#ff0000] [b](!) [/b] [i]Erro ao tentar efetuar login:\nUsuário não encontrado: {msg}")
                
                
                
                
        except Exception as erro:
            msg = erro
            Clock.schedule_once(lambda dt:self.app.gerenciamento_info_geral(f"Erro em class: {__name__} > em def > verificar_login: {msg}\n[color=#ffff00]{traceback.format_exc()}"))
            
            
            
            
    def login_firebase(self, email, senha, verificado=None):
        try:
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.app.api_key}"
            
            payload = {"email":email, "password":senha, "returnSecureToken": True}
            
            resposta = requests.post(url=url, json=payload)
            
            if resposta.status_code ==200:
                dados = resposta.json()
                
                caminho_android = app_storage_path()
            
                caminho_json = os.path.join(caminho_android, "login_usuario.json")
                
                self.app.login_usuario = JsonStore(caminho_json)
                    
                self.app.id_token = dados.get("idToken")
                self.app.refreshToken = dados.get("refreshToken")
                self.app.usuario_uid = dados.get("localId")
                self.app.usuario_logado_email = dados.get("email")
                
                
                self.app.login_usuario.put("auth", token=self.app.id_token, refreshToken=self.app.refreshToken, email=self.app.usuario_logado_email, uid=self.app.usuario_uid)
                
                caminho_root = primary_external_storage_path() + "/win"
                caminho_arquivo = os.path.join(caminho_root, "config.text")
                # dentro de TelaLogin.verificar_login, no bloco if resultado:
                Clock.schedule_once(lambda dt: self.app.verificar_token(id_token=self.app.id_token), 0)

            
                if not os.path.exists(caminho_arquivo):
                    with open(caminho_arquivo, "w") as f:
                        f.write("Primeiro acesso: True")
      
                
                
                    
                    
                Clock.schedule_once(lambda dt: setattr(self.app, "permissao_temporaria_login", True))
                if verificado !=True:
                    Clock.schedule_once(lambda dt: setattr(self.app, "usuario_verificado", None))
                    
                else:
                    Clock.schedule_once(lambda dt: setattr(self.app, "usuario_verificado", True))
                    
                                  
                msg = "[b][color=#00ff00]Login efetuado com sucesso "
                    
                return True, msg
                    
            else:
                dados = resposta.json()
                msg_erro = dados.get('error', {}).get('message', 'Erro desconhecido!')
                if msg_erro =="TOO_MANY_ATTEMPTS_TRY_LATER":

        
                    return False, f"Erro ao tentar fazer login: Muitas tentativas. Tente mais tarde! \nErro: {msg_erro}"
                return False, msg_erro

                
                
                
                
        except Exception as erro:
            msg = erro
            Clock.schedule_once(lambda dt:self.app.gerenciamento_info_geral(f"Erro em class: {__name__} > em def > login_firebase: {msg}\n[color=#ffff00]{traceback.format_exc()}"))
            return False, msg

            
            
        
    def acao_checkbox(self, active):
        pass
        
        
    def mo(self, instance):
        cx_s = self.ids.cx_s
        if instance.icon =="eye":
            instance.icon = "eye-off"
            cx_s.password = False
            #cx_s.password_mask = ""
        elif instance.icon =="eye-off":
            #instance.password_mask = "*"
            instance.icon = "eye"
            cx_s.password = True
        