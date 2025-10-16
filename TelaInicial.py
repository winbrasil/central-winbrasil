from bibliotecas import *



# Tela inicial -------------------- >        
class TelaInicial(Screen):
    def __init__(self, **kwargs):
        
        self.data_sistema = datetime.now().strftime("%d-%m-%y")
        self.win = Window
        self.app = MDApp.get_running_app()
        self.fonte_padrao = self.app.fonte_padrao
        
        self.info_geral_tela_inicial = MDApp.get_running_app().info_geral_build
        self.data_escolhida_picker = self.data_sistema
        
        self.barra_progresso = ProgressBar(value=0)
        
        #self.mostrar_data = MDDatePicker()
        #self.mostrar_data.bind(on_save=self.pegar_date_picker)
        
        super().__init__(**kwargs)
        
        self.lista_geral_mercadorias_oferta = []
        
        
        
        
    def chamar_tela_preco(self):
        db_foto_preco = self.app.db_api.get("winbrasil", {}).get("empresas", {}).get("fpa", {}).get("tabela_preco", {})
        
        lay_principal = self.ids.conteiner_principal
        lay_oferta: MDBoxLayout= self.ids.box_oferta
        
        if db_foto_preco:
            for child in lay_oferta.children[:]:
                lay_oferta.remove_widget(child)
            #lay_central.clear_widgets()
            
            
            
            box_data = MDBoxLayout(orientation="vertical", md_bg_color=(0.05, 0.5, 0, 1), padding=dp(10))
            
            btn_data = MDFillRoundFlatIconButton(text=f"² Alterar data: {self.data_escolhida_picker.replace('-', '/')}", on_release=self.alterar_data_diario, size_hint=(0.8,0.05), pos_hint={"center_x":0.5})
            
            scroll = ScrollView()
            box_data.add_widget(scroll)
            
            box_data_segundario = MDBoxLayout(orientation="vertical", size_hint=(None, None), spacing=dp(10))
            scroll.add_widget(box_data_segundario)
            
            ima = Image(size_hint=(None, None), allow_stretch=True, keep_ratio= False, width=Window.width - dp(20), height=Window.height -dp(20))
            
            box_data_segundario.bind(minimum_size=box_data_segundario.setter("size"))
            
            
 
            box_data_segundario.add_widget(btn_data)
            box_data_segundario.add_widget(ima)
            lay_oferta.add_widget(box_data)
                
            
            link_imagem = db_foto_preco.get(self.data_escolhida_picker, {}).get("link_imagem", None)
            
            if not link_imagem:
                self.app.gerenciamento_info_geral(f"(!) Nenhuma imagem encontrada para essa data. {link_imagem}")
                ima_sem_dados = Image(source="icones/icon_sem_foto_frutas/icon_sem_foto_definida.png", size_hint=(None, None), width=Window.width, height=self.ids.box_oferta.height//1.2, keep_ratio=True, allow_stretch=True)
                #lay_oferta.bind(size=lambda instance, value, ima=ima_sem_dados: ima.pos_hint.update({"center_x":0.1}))
                lay_oferta.add_widget(ima_sem_dados)
                

                
                return
            else:
                self.app.gerenciamento_info_geral(f"(!) imagem válida {link_imagem}")
    
            
            
            def aplicar_imagem(dt):
                
                local = os.path.join(primary_external_storage_path(), f"win/empresas/fpa/tabela_preco/{self.data_escolhida_picker}")
                nome_arquivo = f"tabela_{self.data_escolhida_picker}.jpg"
                
                caminho_completo = os.path.join(local, nome_arquivo)
                
                if os.path.exists(caminho_completo):
                    ima.source = caminho_completo
                    #Clock.schedule_once(lambda dt: self.app.gereciamento_info_geral("Imagem já existe!"))
                else:
                    os.makedirs(local, exist_ok=True)
                    req = requests.get(link_imagem)
                    with open(caminho_completo, "wb") as f:
                        f.write(req.content)
                        #f.reload()
                    
                    ima.source = caminho_completo
                    ima.reload()
                    
            Clock.schedule_once(aplicar_imagem, 0)
                
            
        else:
            box = MDBoxLayout(orientation="vertical")
            imagem = Image(source="icones/icon_sem_conexao/icon_sem_conexao.png")
            box.add_widget(imagem)
            
            lay_oferta.add_widget(box)
            
        
        
        
        
        
        
    def delete_login(self):
        
        try:

            
            if self.app.login_usuario.exists("auth"):
                self.app.login_usuario.delete("auth")  # Apaga os dados de login
                self.app.usuario_verificado = None        # Limpa o status de verificação
                self.app.id_token = None                  # Remove o token atual
                self.app.usuario_logado_email = None      # Remove o email salvo
                self.app.usuario_uid = None               # Remove o UID salvo
                self.app.refreshToken = None              # Remove o refresh token
                self.app.on_start()
                self.organizador_oferta(prosseguir=True)
            else:
                self.app.gerenciamento_info_geral("Login já foi removido!")
                
            
        except Exception as erro:
            msg = erro
            self.app.gerenciamento_info_geral(f"[color=#ff0000]Erro ao deletar autenticação:\n{msg}")

            
        
        
        
        
    def on_touch_down(self, touch):
        box = self.ids.box_lateral_perfil
    
        # Se o box estiver visível e for clicado dentro dele
        if box.opacity > 0 and box.size_hint != (None, None) and box.collide_point(*touch.pos):
            return super().on_touch_down(touch)  # Permite toques nos filhos e bloqueia propagação
    
        # Se estiver visível e o toque for fora dele, oculta
        if box.opacity > 0 and box.size_hint != (None, None):
            box.size_hint = (None, None)
            box.opacity = 0
            box.pos_hint = {"x": -1}
            return True  # Bloqueia propagação do toque
    
        return super().on_touch_down(touch)

        
        
        
        
    def on_touch_move(self, touch):
        if touch.dx > 50:
            if self.ids.box_lateral_perfil:
                self.ids.box_lateral_perfil.size_hint = (None, None)
                self.ids.box_perfil.md_bg_color= (0,0,0,0)
                self.ids.box_lateral_perfil.opacity = 0
                #self.ids.box_lateral_perfil.disabled = True
                self.ids.box_lateral_perfil.pos_hint= {"x":-1}
                return True
                
        return super().on_touch_move(touch)
                
                
        #elif touch.dx < - 60:
#            if self.ids.box_lateral_perfil:
#                self.ids.box_lateral_perfil.size_hint = (0.6, 0.9)
#            
#                self.ids.box_perfil.md_bg_color= (0.1,0.1,1,0.5)
                #self.ids.box_lateral_perfil.opacity = 1
#                return True
                
                
                
                
    def chamar_tela_perfil(self):
        try:
            from main import InfoGeral
            #from main import AnimacaoTextos
            #AnimacaoTextos(instance=self.ids.box_lateral_perfil, duracao=1, tempo=1, repeticao=0)
            if self.ids.box_lateral_perfil:
                if self.ids.box_lateral_perfil.opacity ==0:
                    self.ids.box_lateral_perfil.size_hint = (0.6, 0.89)
                    self.ids.box_lateral_perfil.opacity = 1
                    self.ids.box_lateral_perfil.pos_hint= {"center_x":0.7, "center_y":0.55}
                    
                elif self.ids.box_lateral_perfil:
                    if self.ids.box_lateral_perfil.opacity ==1:
                        self.ids.box_lateral_perfil.size_hint = (None, None)
                        self.ids.box_lateral_perfil.pos_hint= {"center_x":-1}
                        self.ids.box_lateral_perfil.opacity = 0
                        self.ids.box_perfil.md_bg_color = (0,0,0,0)
            
        except Exception as erro:
            msg = erro
            self.app.gerenciamento_info_geral(f" (!) Erro em class: {__class__} > def chamar_tela_perfil: {msg}")

           
        
    def on_pre_enter(self):
        Clock.schedule_once(lambda dt: self.organizador_oferta(), 0)
        
        
        if self.ids:
        
            Clock.schedule_once(lambda dt: (setattr(self.ids.texto_email_perfil, "text", f'[b]Email[/b]: [size={int(sp(12))}] {(self.app.usuario_logado_email if self.app.usuario_logado_email else "N/A")}'), setattr(self.ids.texto_token_perfil, "text", f"[b]Token[/b]:\n {self.app.id_token}"), setattr(self.ids.texto_uid_perfil, "text", f"[b]Uid: [/b]{self.app.usuario_uid}")), 0)
        
                


    def organizador_oferta(self, prosseguir=None):
        db_oferta = self.app.db_api.get("winbrasil", {}).get("telas", {}).get("tela_inicial", {}).get("oferta", {}).get("estatistica", {}).get("mercadorias", {})
        
        db_mimo = self.app.db_api.get("winbrasil", {}).get("empresas", {}).get("fpa", {}).get("clientes", {})
        
        
        
        lista_atuais = sorted([merca for merca in db_oferta.items()])
        
        if sorted(self.lista_geral_mercadorias_oferta) ==lista_atuais:
            return
            #pass
            
        self.lista_geral_mercadorias_oferta = lista_atuais
        

        
        
        lista_items = []
        
        data_rv = []
        
        
        if db_oferta != {} and self.app.usuario_verificado is True:
            
            todas_mercadorias = list(db_oferta.items())
            
            mercadorias_prioridade = [(m, v )for m, v in todas_mercadorias if m.lower().startswith("morango")]
            
            mercadorias_sem_prioridades = [(m,v) for m, v in  todas_mercadorias if not m.lower().startswith("morango")]
            
            mercadorias_ordenada = mercadorias_prioridade + mercadorias_sem_prioridades
            
            for mercadoria, i_dict in mercadorias_ordenada:
                link_merca = i_dict.get("link_icon", None)
                link_icon2 = i_dict.get("link_icon2", None)
                info_data = i_dict.get("info_data", None)
                
                #info_pag = i_dict.get("info_pagamento", {})
                
                
                


# Imagem das mercadorias ------>

                icon = Image(allow_stretch=True, size_hint=(None,None), width=dp(160), height=dp(50))

# < ---------------                
                
                
                
                
                if isinstance(info_data, dict) and len(info_data) >=2:
                    datas_ordenadas = sorted(info_data.keys(), key=lambda d:datetime.strptime(d, "%d-%m-%y"))
                    
                    data_antiga = datas_ordenadas[-2]
                    data_recente = datas_ordenadas[-1]
                    
                    preco_novo = float(info_data[data_recente].get("preco", "0").replace(",", "."))
                    
                    preco_antigo = float(info_data[data_antiga].get("preco", "0").replace(",", "."))
                    
                    diferenca = preco_novo - preco_antigo
                    
                    porcentagem = (diferenca / preco_antigo) * 100 if preco_antigo !=0 else 0
                    
                    if porcentagem >0:
                        texto_indice = f"[b] Subiu {porcentagem:.2f}%"
                        cor_indice = (1,1,1,1)
                        icon_indice = "finance"
                        
                    elif porcentagem < 0:
                       texto_indice = f"[b] Caiu {abs(porcentagem):.2f}%"
                       cor_indice = (0.6,0,0,1)
                       icon_indice = "trending-down"
                       
                    else:
                       texto_indice = "[b] Estável"
                       
                       
                data_rv.append({"url_icon": link_merca or link_icon2 or "", "nome_merca": mercadoria.upper(), "acao_ir_loja": partial(self.ir_para_loja_com_scroll, mercadoria), "preco_antigo": f'{preco_antigo}', "preco_recente": f"{preco_novo}", "indic_texto": texto_indice, "indic_cor": cor_indice,"indic_icon": icon_indice, "data_antiga": data_antiga, "data_recente": data_recente})
            
            
                lista_items.append((link_merca, link_icon2, icon, mercadoria, link_merca, mercadoria))
                
                self.app.tela_compras._ativa = True

                
            self.app.tela_compras.pre_dowloads_icon(lista_items)
            
            self.ids.rv_oferta.data = data_rv
            
            
            self.ids.box_filho_mimos.clear_widgets()
            self.ids.box_filho_mimos.add_widget(Image(source="icones/icon_em_construcao/icon_em_construcao2.png", keep_ratio= True, allow_stretch=True))
            
# < ---------
            
            
    def dia_ate_dia(self, dia_alvo: int, hoje: date | None=None) -> int:
        
        hoje = hoje or date.today()
        if hoje.day <= dia_alvo:
            return dia_alvo - hoje.day
            
        dias_mes = monthrange(hoje.year, hoje.month)[1]
        
        return (dias_mes - hoje.day) + dia_alvo
        
        
        
    
    def ir_para_loja_com_scroll(self, nome_mercadoria):
            self.app.mercadoria_destino = nome_mercadoria
            self.app.root.current = "tela_compras"
            
            
            
            
            
            
            
            
            
            
            
                        
            
    def encaminhamento_seguro_login(self, instance, box=None):
        try:
            if self.app.usuario_verificado is None:
                Clock.schedule_once(lambda dt:self.app.gerenciamento_info_geral(msg="[color=#ff0000](!) Necessário fazer login!"), 0)
                    
                Clock.schedule_once(lambda dt: self.app.info_geral_build.dismiss(), 15)
                    
                self.app.root.current = "pre_tela_login"
                self.app.root.get_screen("tela_sair").historico_telas.append("pre_tela_login")
            else:
                if box =="inicial":
                    
                    Builder.unload_file("tela_inicial.kv")
                    Builder.load_file("tela_inicial.kv")
                    
                    box_oferta = self.ids.box_oferta
                    
                    for child in box_oferta.children[:]:
                        box_oferta.remove_widget(child)
                        
                    self.lista_geral_mercadorias_oferta = []
                        
                    self.organizador_oferta()
                    
                    setattr(self.app.root, "current", "tela_inicial")
                    
                if box =="preço":
                    self.chamar_tela_preco()
                    
                if box == "OS":
                    setattr(self.app.root, "current", "tela_os")
                    
                if box =="compras":
                    setattr(self.app.root, "current", "tela_compras")
                    #self.app.gerenciamento_info_geral(msg="[color=#ff0000](!) compras")
                    
                if box =="perfil":
                    self.chamar_tela_perfil()
                    
                
                    
                box_clicado = instance.parent
                barra = self.ids.box_barra_inferior
                
                for box in barra.children:
                    box.md_bg_color= 0,0,0,0
                        
                box_clicado.md_bg_color = (1,1,1,0.2)
                
                    

                    
                
                
        except Exception as erro:
            msg_erro = erro
            self.app.gerenciamento_info_geral(msg=msg_erro)
    
    

            
    def atua_textsize(self, instance, width ):
        instance.text_size = (width - dp(10), None)

            
            
    def alterar_data_diario(self, instance):
        
        
        self.mostrar_data = MDDatePicker()
        
        self.mostrar_data.bind(on_save=partial(self.pegar_date_picker, instance))
        
        self.mostrar_data.open()
        
        
        
    def pegar_date_picker(self, instance_btn,instance_datepicker=None, value=None, *args):
        data_formatada = value.strftime("%d-%m-%y")
        
        self.data_escolhida_picker = data_formatada
        if instance_btn.text[0] == "²":
            
        
            instance_btn.text = f"² Alterar data: [b]{self.data_escolhida_picker}".replace("-", "/")
            self.chamar_tela_preco()
        
        
        if self.app.usuario_verificado:
            pass
        
            #self.diario_oficial()
        else:
            Clock.schedule_once(lambda dt: self.app.gerenciamento_info_geral("(!) Usuário não está verificado!"), 1)
            
            self.app.root.current = "pre_tela_login"
            
            
    def atualizar_app(self):
        try:
            from main import InfoGeral
            from main import AnimacaoTextos
            popup = InfoGeral(arg="")
            versao_nome, versao_code = self.app.obter_versao_sdk()
            
            if not  isinstance(versao_nome, float):
                versao_nome = 0.1
                
            db_versao = self.app.db_api.get("winbrasil", {}).get("versao")
            
            if db_versao:
                versao_anterior = db_versao.get("versao_anterior", "Erro ao obter versão")
                versao_atual = db_versao.get("versao_atual", "Erro ao obter versão")
                db_info_versao = db_versao.get("info_versao", "N/A")
                if float(versao_nome) < float(versao_atual):
                    self.ids.versao_sdk.text= f"[color=#00ff00] • [/color]Atualização disponível!\nversão nova: {versao_atual}\nClick para mais informações "
                    popup.texto_info_geral.text= f"[b][color=#00ff00]Eba! Nova versão disponível:[/b][/color]\nsua versão: [i]{versao_nome}[/i]\n versão disponível: [i]{versao_atual}\n • Informações da atualização:\n[color=ffff00] - {db_info_versao}"
                    popup.texto_info_geral.texture_update()
                    popup.atua_tam_fonte()
                    popup.open()
                    #AnimacaoTextos(instance=popup.texto_info_geral, duracao=2, tempo=1)
                else:
                    popup = InfoGeral()
                    popup.texto_info_geral.text = f"Erro ao obter dados de atualização, db: {db_versao}"
                    popup.texto_info_geral.texture_update()
                    popup.atua_tam_fonte()
                    popup.open()
                    Clock.schedule_once(lambda dt: popup.dismiss(), 0.4)
        except Exception as erro:
            msg = erro
            self.app.gerenciamento_info_geral(f"(!) Erro em class: {__class__} > def atualizar_app: {msg}\n[color=#ffff00] - {traceback.format_exc()}")

class OrgMerca(MDBoxLayout, RecycleDataViewBehavior):
    
    url_icon = StringProperty("")
    nome_merca = StringProperty("")
    preco_antigo = NumericProperty(0.0)
    preco_recente = NumericProperty(0.0)
    data_antiga = StringProperty("")
    data_recente = StringProperty("")
    indic_texto = StringProperty("")
    indic_cor = ListProperty([1,1,1,1])
    
    indic_icon = StringProperty("")
    acao_ir_loja = ObjectProperty(allownone=True)
    
    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)
        
        
    def refresh_view_attrs(self, rv, index, data):
         ret = super().refresh_view_attrs(rv, index, data)
         
         try:
             img = self.ids.get("img")
         except Exception as erro:
             img = None
         img.texture = None
         img.source = ""
         
         if img and self.url_icon:
             self.app.tela_compras.downloads_icon(url=self.url_icon if self.url_icon else None, icon= img, merca=self.nome_merca)
         else:
             img.source = "icones/icon_sem_foto_frutas/icon_sem_foto_definida.png"
             
         return ret
         
         
         
    def disparar_ir_loja(self):
         cb = self.acao_ir_loja
         if callable(cb):
             cb()
             
             