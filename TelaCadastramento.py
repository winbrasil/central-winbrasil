from bibliotecas import *

class TelaCadastramento(Screen):
    def __init__(self, **kwargs):
        self.tela_x = Window.width
        self.app = MDApp.get_running_app()
        self.win = Window
        self.fonte_padrao = self.app.fonte_padrao

        super().__init__(**kwargs)
        
    def on_enter(self):
        for widgets in self.walk():
            if isinstance(widgets, TextInput):
                cx_s1 = self.ids.cx_s1
                cx_s2 = self.ids.cx_s2
                if widgets in (cx_s1, cx_s2):
                    widgets.text = ""
        

        
        
        
    def verificar_cadas(self):
        try:
            cx_u = self.ids.cx_u.text.strip()
            cx_e = self.ids.cx_email.text.strip()
            cx_c = self.ids.cx_contato.text.strip()
            cx_s1 = self.ids.cx_s1.text.strip()
            cx_s2 = self.ids.cx_s2.text.strip()
            
            
            
            campos = {
                "cx_u": {"min_len": 6, "tipo": "texto"},
                "cx_email": {"tipo": "email"},
                "cx_contato": {"tipo": "telefone"},
                "cx_s1": {"min_len": 6, "tipo": "senha"},
                "cx_s2": {"min_len": 6, "tipo": "senha"},
            }
    
            erro = False
    
            for campo_id, regra in campos.items():
                campo = self.ids[campo_id]
                texto = campo.text.strip()
    
                cor_erro = (1, 0, 0, 1)
                cor_ok = (1, 1, 1, 1)
    
                # Verifica vazio
                if not texto:
                    campo.canvas.before.children[7].rgba = cor_erro
                    erro = True
                    continue
    
                # Verifica tipo de validação
                if regra.get("tipo") == "email":
                    if not texto.endswith("@gmail.com"):
                        campo.canvas.before.children[7].rgba = cor_erro
                        erro = True
                        continue
    
                elif regra.get("tipo") == "telefone":
                    if not (texto.isdigit() and len(texto) == 11):
                        campo.canvas.before.children[7].rgba = cor_erro
                        erro = True
                        continue
    
                elif regra.get("min_len"):
                    if len(texto) < regra["min_len"]:
                        campo.canvas.before.children[7].rgba = cor_erro
                        erro = True
                        continue
    
                # Se passou, cor branca
                campo.canvas.before.children[7].rgba = cor_ok
    
            if erro:
                self.app.gerenciamento_info_geral("[b](!) Erro:[/b] Verifique os campos obrigatórios!")
                Clock.schedule_once(lambda dt: self.app.info_geral_build.dismiss(), 3)
                
                
                
            else:
                #th = threading.Thread(target=self.login_firebase(email=cx_e, senha=cx_s1), daemon=True)
                #th.start()
                th = threading.Thread(target= lambda :self.criar_usuario_firebase(email=cx_e, senha=cx_s1) , daemon=True)
                th.start()
                
                self.app.gerenciamento_info_geral("Aguarde...")
                
                    


                    
    
        except Exception as e:
            self.app.gerenciamento_info_geral(
                f"Erro em class TelaCadastramento > verificar_cadas:\n{e}\n{traceback.format_exc()}")
                
    #def criar_usuario(usuario=None, )

        
    def registrar_novo_usuario(self):
        try:
            usuario = self.ids.cx_u.text.strip()
            senha = self.ids.cx_s1.text.strip()
            email = self.ids.cx_email.text.strip()
            contato = int(self.ids.cx_contato.text.strip())
            
            dados_usuario = {usuario: senha}
            dados_email = {usuario: email}
            dados_contato = {usuario: contato}
            
            
    
            url_base = f"{self.app.link_api}/winbrasil/empresas/fpa"
            #from main import InfoGeral
            #Clock.schedule_once(lambda dt: InfoGeral(arg=url_base).open(), 1)
    
            respostas = [
                requests.put(f"{url_base}/usuarios/{usuario}.json?auth={self.app.id_token}", data=json.dumps(dados_usuario)),
                requests.put(f"{url_base}/emails_usuarios/{usuario}.json?auth={self.app.id_token}", data=json.dumps(dados_email)),
                requests.put(f"{url_base}/contatos/{usuario}.json?auth={self.app.id_token}", data=json.dumps(dados_contato)),
            ]
    
            if all(r.status_code == 200 for r in respostas):
                Clock.schedule_once(lambda dt: self.app.gerenciamento_info_geral(
                    f"[b][color=#00ff00](!)[/b] Usuário: {usuario} cadastrado com sucesso"), 0)
    
                Clock.schedule_once(lambda dt: self.app.info_geral_build.dismiss(), 3)
                Clock.schedule_once(lambda dt: setattr(self.app.root, "current", "tela_login"), 2)
    
            else:
                erros = [r.status_code for r in respostas if r.status_code != 200]
                Clock.schedule_once(lambda dt: self.app.gerenciamento_info_geral(
                    f"[b][color=#ff0000]Erro[/color][/b] ao cadastrar usuário. Códigos HTTP: {erros}"), 0)
                Clock.schedule_once(lambda dt: self.app.info_geral_build.dismiss(), 5)
                
                
    
        except Exception as erro:
            msg = erro
            Clock.schedule_once(lambda dt: self.app.gerenciamento_info_geral(
                f"[b][color=#ff0000]Erro:[/color][/b] {msg}"), 0)
                
                
    
            
    def criar_usuario_firebase(self, email, senha, auto_criar=None ):
        try:
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.app.api_key}"
    
            payload = {
                "email": email,
                "password": senha,
                "returnSecureToken": True
            }
    
            resposta = requests.post(url, json=payload)
            dados = resposta.json()
    
            if resposta.status_code == 200:
                #Clock.schedule_once(lambda dt: self.app.gerenciamento_info_geral(msg=f"[b][color=#00ff00]Cadastro efetuado com sucesso "), 0)
    
                if "idToken" in dados:
                    self.app.id_token = dados["idToken"]
                    
                    self.app.usuario_logado_email = dados["email"]
                    self.app.usuario_uid = dados["localId"]
                    self.app.refreshToken = dados["refreshToken"]
                    
                    
                    
                    #th = threading.Thread(target=self.app.db, daemon=True)
                    #th.start()
                    
                    def verificar_dados(dt):
                        try:
                            #self.app.login_usuario = JsonStore("login_usuario.json")
                            #self.app.login_usuario.put("auth", token=self.app.id_token, email=self.app.usuario_logado_email, uid=self.app.usuario_uid, refreshToken=self.app.refreshToken)
        
                            #Clock.schedule_once(lambda dt: setattr(self.app, "permissao_temporaria_login", True))
                    
                    # Inicia carregamento do banco (thread)
                           
                            if self.app.db_api:
                                
                                
                                verificacao_conta = Autenticacao(
                                    modo="gmail",
                                    fonte_padrao=self.fonte_padrao,
                                    db_api=self.app.db_api,
                                    cx_u=self.ids.cx_u.text.strip(),
                                    cx_s=senha,
                                    cx_email=email
                                )
                                verificacao_conta.open()
                                #Clock.schedule_once(lambda dt: self.app.gerenciamento_info_geral(f" else: self.db_api: {self.app.db_api}"), 2)
                                
                                #Clock.schedule_once(verificar_dados, 1)
                            else:
    
                                #Clock.schedule_once(lambda dt: self.app.gerenciamento_info_geral(f" else: self.db_api: {self.app.db_api}"), 5)
                                Clock.schedule_once(verificar_dados, 1)
        
                        except Exception as erro:
                            msg = erro
                            Clock.schedule_once(lambda dt:self.app.gerenciamento_info_geral(
                                f"Erro em class: {__name__} > def verificar_dados:\n{msg}"), 0)
                            
                            
                    Clock.schedule_once(verificar_dados, 1)
                    
                    
                else:
                    erro = dados.get("error").get("message", "Erro desconhecido!")
                    
                    
            else:
                Clock.schedule_once(lambda dt: self.app.gerenciamento_info_geral(msg=f"[color=#ff0000][b](!)[/b] [i]Erro ao cadastrar usuário!\n [color=#ffff00]cod: [i]{resposta.status_code}![/i] \nPossíveis causas: email ou usuário já existe! "), 0)
                
    
                # Função para aguardar o db carregar
                
    
                
    
        except Exception as erro:
            msg = erro
            Clock.schedule_once(lambda dt: self.app.gerenciamento_info_geral(
                f"(!) Erro em class: {__name__} > def login_firebase:\n{msg}"), 0)





class Autenticacao(Popup):
    def __init__(self, tela=None, modo=None, fonte_padrao =None, db_api=None, cx_email=None, cx_u=None,cx_s=None, **kwargs):
        #self.app = MDApp.get_running_app()
        self.fonte_padrao = fonte_padrao
        
        super().__init__(**kwargs)
        
        
        
        self.app = MDApp.get_running_app()
        self.cont_reenviar_codigo = 30
        self.db_api = db_api
        self.cx_email = cx_email
        self.cx_u = cx_u
        
        
        #self.border = (dp(2),0, dp(5), dp(20))
        self.background_color = (0, 0, 0, 0)
        self.size_hint= (1, 0.4)
        #self.pos_hint= {"center_x":0.5, "center_y":0.25}
        self.title_align= "center"
        self.title = ""
        self.separator_height = 0
        self.auto_dismiss = False
        
        with self.canvas.before:
            Color(0.2, 0, 1, 1)
            rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(40)])
            Color(1,1,1,1)
            linha = Line(rounded_rectangle=[self.x, self.y, self.width, self.height, dp(40)], width=dp(1))
        self.bind(pos=lambda instance, value, rect=rect, linha=linha: (setattr(rect, "pos", instance.pos), setattr(linha, "rounded_rectangle", [instance.x, instance.y, instance.width, instance.height, dp(40)])),
        
            size=lambda instance, value, rect=rect, linha=linha: (setattr(rect, "size", instance.size), setattr(linha, "rounded_rectangle", [instance.x, instance.y, instance.width, instance.height, dp(40)])))
        
        
        self.box_conteiner_principal = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(15))
        self.content = self.box_conteiner_principal
        with self.box_conteiner_principal.canvas.before:
            Color(0.2, 0.2, 0.4, 0.2)
            rect = RoundedRectangle(pos=self.box_conteiner_principal.pos, size=self.box_conteiner_principal.size, texture=self.app.criar_gradient_texture(), radius=[dp(50)])
            
        self.box_conteiner_principal.bind(pos=lambda instance, value, rect=rect:( setattr(rect, "pos", instance.pos), setattr(rect, "radius", [dp(50)])),
        
            size=lambda instance, value, rect=rect: ( setattr(rect, "size", instance.size), setattr(rect, "radius", [dp(50)])))
        
        
        
        self.box_segundario = BoxLayout(orientation="vertical", size_hint=(1, None))
        info_by = Label(markup=True,text=f"[size={min(int(sp(50)), int(self.fonte_padrao))}]V[/size]erificação via [b]{modo.upper()}[/b].", size_hint=(1, None))
        
        self.box_segundario.bind(minimum_height=self.box_segundario.setter("height"))
        
        self.box_segundario.add_widget(info_by)
        self.box_conteiner_principal.add_widget(self.box_segundario)
        
        self.box_cx_entradas = BoxLayout(orientation="horizontal", padding=dp(10), spacing=dp(20))
        self.box_conteiner_principal.add_widget(self.box_cx_entradas)
        
        self.cx_1 = TextInput()
        self.cx_2 = TextInput()
        self.cx_3 = TextInput()
        self.cx_4 = TextInput()
        self.lista_cxs_codigos = [self.cx_1, self.cx_2, self.cx_3, self.cx_4]
        
        for cx in self.lista_cxs_codigos:
            self.box_cx_entradas.add_widget(cx)
            cx.background_color= (0,0,0,0)
            cx.font_size= min(sp(60), self.fonte_padrao *1.3)
            cx.multiline = False
            cx.input_filter = "int"
            cx.input_type = "number"
            cx.valign= "middle"
            cx.halign= "center"
            
            cx.bind(text=self.limitar_valor)
            
            with cx.canvas.before:
                Color(1, 1, 1, 1)
                
                
                rect = RoundedRectangle(pos=cx.pos, size=cx.size, radius=[dp(30)])
                Color(1,1,0,1)
                
                
                linha = Line(rounded_rectangle=[cx.x, cx.y, cx.width, cx.height, dp(0)], width=dp(1))
                Color(0.2,0,0.4,1)
                
                
            cx.bind(pos=lambda instance, value, rect=rect, linha=linha: (setattr(rect, "pos", instance.pos), setattr(linha, "rounded_rectangle", [instance.x, instance.y, instance.width, instance.height, dp(35)])),
                size=lambda instance, value, rect=rect, linha=linha: (setattr(rect, "size", instance.size), setattr(linha, "rounded_rectangle", [instance.x, instance.y, instance.width, instance.height, dp(35)])))
                
                
        box_botao_verificar = BoxLayout(orientation="vertical", padding=dp(10))
        self.box_conteiner_principal.add_widget(box_botao_verificar)
        
                
                
                
        self.btn_verificar_conta = MDRectangleFlatButton( text="Verificar", size_hint=(1,1), on_release=self.verificar_codigo)
        
        box_botao_verificar.add_widget(self.btn_verificar_conta)
        
        
        self.box_voltar_tempo = BoxLayout(orientation="horizontal", padding=dp(10), spacing=dp(20), size_hint=(1, None))
        self.box_voltar_tempo.bind(minimum_height=self.box_voltar_tempo.setter("height"))
        
        self.box_conteiner_principal.add_widget(self.box_voltar_tempo)
        with self.box_voltar_tempo.canvas.before:
            Color(0.2, 0.3, 0.2, 0.2)
            rect = RoundedRectangle(pos=self.box_voltar_tempo.pos, size=self.box_voltar_tempo.size, radius=[dp(50)])
            
        self.box_voltar_tempo.bind(pos=lambda instance, value, rect=rect:(setattr(rect, "pos", instance.pos), setattr(rect, "radius", [dp(30)])),
            size=lambda instance, value, rect=rect: (setattr(rect, "size", instance.size), setattr(rect, "radius", [dp(30)])))
            
            
            
        btn_voltar = MDRaisedButton(markup=True, text="[b]VOLTAR", size_hint=(1, None), height=min(dp(50), Window.height * 0.05), on_release=lambda dt: self.dismiss())
        
        self.btn_reenviar_codigo = MDRaisedButton(markup=True, text="[b]REENVIA CODIGO",  size_hint=(1,None), height=min(dp(50), Window.height * 0.05), on_release= self.andamento_codigo)
        self.box_voltar_tempo.add_widget(btn_voltar)
        self.box_voltar_tempo.add_widget(self.btn_reenviar_codigo)
        self.andamento_codigo()
        
        
    def limitar_valor(self,instance, value):
        try:
            if len(value) >2:
                instance.text = value[:2]
                Clock.schedule_once(lambda dt: self.app.gerenciamento_info_geral("[color=#ff0000]Somente 2 números por campo[/color]"), 0)
                Clock.schedule_once(lambda dt: self.app.info_geral_build.dismiss(), 2)
        except Exception as erro:
            msg = erro
            self.app.gerenciamento_info_geral(f"Erro em class Autenticacao > def limitar_valor: {msg} ")
        
            
            
    def andamento_codigo(self, *args):
        try:
            if self.cont_reenviar_codigo ==30:
                self.btn_reenviar_codigo.text = f"[b] REENVIAR CODIGO EM {self.cont_reenviar_codigo:2d}"
                
                
                self.parar_cont_codigo = Clock.schedule_interval(lambda dt: self.suplimento_andamento_codigo(), 1)
                self.btn_reenviar_codigo.disabled = True
                
                th = threading.Thread(target=self.enviar_codigo_email, daemon=True)
                th.start()
                
                self.app.gerenciamento_info_geral('[b](!) Aguarde ...')
                Clock.schedule_once(lambda dt: self.app.info_geral_build.dismiss(), 3)
                
                
            
        except Exception as erro:
            msg = erro
            self.app.gerenciamento_info_geral(f"Erro em class autenticacao > def andamento_codigo: {msg}")
            
            
            
    
    def suplimento_andamento_codigo(self):
            try:
                self.cont_reenviar_codigo -=1
                self.btn_reenviar_codigo.text = f"[b] REENVIAR CODIGO EM {self.cont_reenviar_codigo:2d}"
                if self.cont_reenviar_codigo <=0:
                    self.cont_reenviar_codigo = 30
                    self.parar_cont_codigo.cancel()
                    self.btn_reenviar_codigo.disabled = False 
                    self.btn_reenviar_codigo.text = f"[b] REENVIAR CODIGO"
                    
            except Exception as erro:
                msg = erro
                Clock.schedule_once(lambda dt: self.app.gerenciamento_info_geral(f"Erro em class Autenticacao > def suplimento_andamento_codigo: {msg}"), 0)
                
                
    def enviar_codigo_email(self):
        try:
            self.db_api = MDApp.get_running_app().db_api
            # Gera código de verificação como lista de strings formatadas com dois dígitos
            codigo_verificacao = [str(random.randint(0, 99)).zfill(2) for _ in range(4)]
            self.codigo_enviado_email = codigo_verificacao
    
            # Coleta o email e senha do remetente
            email_remetente = self.db_api.get("winbrasil", {}).get("email", {})
            email = email_remetente.get("gmail", "ola.winbrasil@gmail.com")
            senha = email_remetente.get("senha")
    
            remetente = email
            senha_app = senha
    
            # Prepara o email
            mensagem = MIMEMultipart()
            mensagem["From"] = remetente
            mensagem["To"] = self.cx_email
            mensagem["Subject"] = "(!) Seja bem-vindo (a) ao WinBrasil"
    
            # Junta os 4 dígitos com espaço
            codigos_juntos = " ".join(codigo_verificacao)
    
            corpo_html = f"""
            <html>
                <body>
                    <h2 style="color: #2E86C1;">Olá {self.cx_u.upper()},</h2>
                    <p>Seu código de verificação é:</p>
                    <h1 style="color: #e74c3c; font-size: 32px;">{codigos_juntos}</h1>
                    <p>Insira este código no aplicativo para concluir seu cadastro.</p>
                    <p>Atenciosamente,<br>Equipe WinBrasil</p>
                </body>
            </html>
            """
    
            mensagem.attach(MIMEText(corpo_html, "html"))
    
            # Envia o email via SMTP Gmail
            servidor = smtplib.SMTP("smtp.gmail.com", 587)
            servidor.starttls()
            servidor.login(remetente, senha_app)
            servidor.sendmail(remetente, self.cx_email, mensagem.as_string())
            servidor.quit()
    
            Clock.schedule_once(lambda dt: self.app.gerenciamento_info_geral("[b][color=#2ECC71]Código enviado com sucesso para seu e-mail!"), 0)
            
            Clock.schedule_once(lambda dt:self.app.info_geral_build.dismiss(), 2)
        
        except Exception as erro:
            msg = erro
            Clock.schedule_once(lambda dt: self.app.gerenciamento_info_geral(f"Erro em class TelaCadastramento > def enviar_codigo_email: {msg}\n[color=#ffff00]{traceback.format_exc()}"), 0)
    
            
            
    def dados_codigo(self, cod):
        try:
            self.codigo_enviado_email = cod
            
        except Exception as erro:
            msg = erro
            self.app.gerenciamento_info_geral(f"Erro em class Autenticacao > def dados_codigo: {msg}")
            
            
            
            
    def verificar_codigo(self, *args):
        try:
            # Captura os 4 valores digitados e formata com dois dígitos
            codigo_digitado = [cx.text.strip().zfill(2) for cx in self.lista_cxs_codigos]
    
            # Verifica se foi recebido um código por e-mail
            if not hasattr(self, "codigo_enviado_email"):
                self.app.gerenciamento_info_geral("[b][color=#ff0000]Código ainda não foi gerado ou enviado.")
                return
    
            # Verifica igualdade dos códigos
            if codigo_digitado == self.codigo_enviado_email:
                self.app.gerenciamento_info_geral("[b][color=#2ECC71]Código verificado com sucesso!")
                
                Clock.schedule_once(lambda dt: setattr(self.app, "permissao_temporaria_login", True))
                
                Clock.schedule_once(lambda dt: setattr(self.app, "usuario_verificado", True))
                th = threading.Thread(target=self.app.db, daemon=True)
                th.start()
                
                # prossegue com o cadastro
                Clock.schedule_once(lambda dt: self.dismiss(), 2)
                
                
                
                Clock.schedule_once(lambda dt: threading.Thread(target=self.app.root.get_screen("tela_cadastramento").registrar_novo_usuario, daemon=True).start(),0.2)

    
            else:
                self.app.gerenciamento_info_geral("[b][color=#E74C3C]Código incorreto. Tente novamente.")
    
        except Exception as erro:
            msg = erro
            self.app.gerenciamento_info_geral(f"Erro em verificar_codigo:\n{msg}")