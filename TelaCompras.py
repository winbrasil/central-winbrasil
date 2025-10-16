

from bibliotecas import *

class TelaCompras(Screen):
    def __init__(self, **kwargs):
        from main import InfoGeral
        
        self.pop = InfoGeral(modo="carregamento")
        self.app = MDApp.get_running_app()
        
        self.cont_items_compras = 0
        #self.quant_merca = 1
        
        super().__init__(**kwargs)
        self.lista_mercadoria_carrinho = {}
        self.lista_merca_inverso = {}
        
        self.lista_geral_mercadorias_compras = []
        
        
        
        
       
    def on_pre_enter(self):
        self._ativa = True
        from main import InfoGeral
        
        
        th = threading.Thread(target=self.efeito_carregamento, daemon=True)
        th.start()
        
        
    def efeito_carregamento(self):
        
        Clock.schedule_once(lambda dt: setattr(self.pop, "texto_info_geral.color", (0,1,1,1)))
        #self.pop.background_color= (0, 0, 0.4)
        Clock.schedule_once(lambda dt:setattr(self.pop, "pos_hint", {"y": 0.3}))
        
        Clock.schedule_once(lambda dt:self.pop.open())
        
        
        
    def on_enter(self):
        
        
        
        Clock.schedule_once(lambda dt:self.organizar_mercadorias(), 0)
        
        Clock.schedule_once(self.scroll_ate_mercadoria_destino, 0)
        
    def on_leave(self):
        self._ativa = False
        self.ids.scroll_compras.scroll_y = 1
        
        #Clock.schedule_once(lambda dt: self.ids.box_merca_filho.clear_widgets(), 0)
        
        
    def scroll_ate_mercadoria_destino(self, dt):
        
        destino = self.app.mercadoria_destino
        if not destino:
            return
        scroll = self.ids.scroll_compras
        box_geral = self.ids.box_merca_filho
        
        for widget in reversed(box_geral.children):
            if hasattr(widget, "nome_mercadoria") and widget.nome_mercadoria ==destino:
                scroll.scroll_to(widget)
                Clock.schedule_once(lambda dt: toast(f"{destino} localizado"), 0.1)
                break
                # Após scroll
        

            
            
        
        
        
        
    def organizar_mercadorias(self):
        try:
            
            
            
            
            from main import InfoGeral
            if self.app.root.current =="tela_compras":
            
    
                
                db = MDApp.get_running_app().db_api
                
                
                box_pai = self.ids.box_merca_filho

                
                items = []
                if db:
                    db_mercadorias = db.get("winbrasil", {}).get("empresas", {}).get("fpa", {}).get("estoque", {}).get("mercadorias", {})
                    
                    lista_atuais = sorted([merca for categoria, mercadorias in db_mercadorias.items() for merca in mercadorias])
                    
                    if sorted(self.lista_geral_mercadorias_compras) == lista_atuais:
                        self.pop.dismiss()
                        return
                        
                        
                    self.lista_geral_mercadorias_compras = lista_atuais
                    
                    box_pai.clear_widgets()
                    
                    for categoria, merca_dict in db_mercadorias.items():
                        
                        for merca, esp_dict in merca_dict.items():
                            info_preco = esp_dict.get("preco", "N/A")
                            link_icon = esp_dict.get("link_icon", None) 
                            link_icon2 = esp_dict.get("link_icon2", None)
                            
                            esp = esp_dict.get("esp", None) 
                            
                            
                            #esp_info = esp.get("tipo", "N/A")
                            
                            
                            info_tipo_cali = esp.get("cali", None) if esp else ["N/A"]
                            
                            

                                
                                
                                
                            box_conteiner_principal = MDBoxLayout(orientation="vertical", padding=dp(10), spacing=dp(1), md_bg_color=(1,1,1,1), size_hint=(1, None), radius=[dp(20)])
                            box_conteiner_principal.nome_mercadoria = merca
                            
                            box_info_frame_encima = MDBoxLayout(orientation="horizontal", size_hint=(1, None), spacing=dp(10), md_bg_color=(1,1,1,1))
                            
                            box_info_frame_encima.nome_mercadoria = merca
                            
                            box_frame_meio = MDBoxLayout(orientation="horizontal", size_hint=(1, None), padding=dp(5), spacing=dp(10), md_bg_color=(1, 1, 1, 0.2), height=dp(40))
                            
                            
                            box_info_frame_embaixo = MDBoxLayout(orientation="horizontal", spacing=dp(5), padding=dp(5), size_hint=(1, None), md_bg_color=(1,1,1,1))

#items frame ecima ----- >
                            icon= AsyncImage(size_hint=(0.4, None), allow_stretch=True, height=dp(50))
                            
                            with icon.canvas.before:
                                Color(0, 1, 0, 0.4)
                                rect = RoundedRectangle(pos=icon.pos, size=icon.size, radius=[dp(30), 0, dp(30), 0])
                            icon.bind(pos= lambda instance,value, rect=rect: setattr(rect, "pos", instance.pos), size=lambda instance, value, rect=rect: setattr(rect, "size", instance.size))
                            
                            
                            
                            
                            label_info_mercadoria = MDLabel( text=f"{merca}".upper(), font_style="H6", size_hint=(0.5, None), height=dp(40))

# < -----------

# items frame meio --------- >
                            box_quant_frame_meio = MDBoxLayout(orientation="horizontal", size_hint=(None, None), md_bg_color=(0.5,1,1,0.2), padding=dp(5))
                            
                            
                            
                            
                            
                            
# items box separado, box quant_frame_meio -- >

                            quant_merca = 1
                            label_quant = MDLabel(text="quant.", size_hint=(None, None), halign="left", valign="middle", width=dp(46))
                            
                            #label_quant.bind(texture_size=lambda instance, value: setattr(instance, "size", value))
                            
                            btn_diminuir = MDIconButton(icon="minus", theme_icon_color="Custom", icon_color=(1,0,0,1), size_hint=(None, None), pos_hint={"center_y":0.6}, icon_size=dp(20), height=dp(15), width=dp(15))
                            
                            cx_alterar_quant = MDTextField(text=f"{quant_merca}", size_hint=(None, None), size=(dp(20), dp(20)), pos_hint={"center_y": 0.6}, halign="center", input_type="number")
                            
                            
                            
                            btn_acrescentar = MDIconButton(icon="plus", theme_icon_color="Custom", icon_color=(0,1,0,1), size_hint=(None, None), pos_hint={"center_y":0.6}, icon_size=(dp(20)), height=dp(15), width=dp(5))
                            
                            if esp and isinstance(info_tipo_cali, dict):
                                esp_cali = next(iter(info_tipo_cali))
                                texto = ",".join(f"{cop}.{esp_cali}"for cop in esp)
                            else:
                                texto = "N/A"
                            
                            btn_esp = MDFillRoundFlatButton(text=f"Espe: {texto}", size_hint=(0.5, None), theme_text_color=("Custom"), md_bg_color=(0, 0.4, 0, 1))
                            
                            if isinstance(info_tipo_cali, dict) and info_tipo_cali:
                                menu_items= [{"text": f"{','.join(esp) if esp else 'N/A'}.{c}", "on_release": lambda esp_info=esp if esp else "N/A", x=c: self.set_items(x)} for c in info_tipo_cali] #if info_tipo_cali else "N/A"
                            else:
                                menu_items = [{"text": "N/A", "on_release": lambda : self.set_items("N/A")}]
                            
                            menu = MDDropdownMenu(caller=btn_esp, items=menu_items, size_hint=(None, None), max_height=dp(200), width_mult=4, size=(dp(100), dp(30)))
                            
                            
                            
                            btn_esp.bind(on_release= lambda instance, m=menu: m.open())
                            
                            
                            box_quant_frame_meio.add_widget(label_quant)
                            box_quant_frame_meio.add_widget(btn_diminuir)
                            
                            box_quant_frame_meio.add_widget(cx_alterar_quant)
                            
                            box_quant_frame_meio.add_widget(btn_acrescentar)
                            
                            #box_frame_meio.add_widget(label_quant)
                            box_frame_meio.add_widget(box_quant_frame_meio)
                            box_frame_meio.add_widget(btn_esp)
                            
                            #box_frame_meio.add_widget(menu)
                            
                            box_quant_frame_meio.bind(minimum_width=box_quant_frame_meio.setter("width"), minimum_height=box_frame_meio.setter("height"))
# < --------------
                            
# < ------- items frame_meio
# items frame embaixo ------- >
                            label_preco = MDLabel(markup=True, text=f"Valor: [color=#00ff00][b]{info_preco}", size_hint=(1, None),halign="right")
                            
                            btn_add = MDFillRoundFlatIconButton(icon="plus", text="adicionar ao carrinho", halign="left",valign="bottom", md_bg_color=(0,0,0,0), text_color=(0,1,0,1), icon_color=(0,1,0,1), size_hint=(None, None), on_release=lambda instance, info_preco=info_preco, label_preco=label_preco.text, cx_alterar_quant=cx_alterar_quant,merca=merca: self.add_carrinho(merca, info_preco, label_preco, cx_alterar_quant))

# < -----------
                            
                            
                            
                            
                            box_pai.add_widget(box_conteiner_principal)
                            
                            box_conteiner_principal.add_widget(box_info_frame_encima)
                            
                            box_conteiner_principal.add_widget(box_frame_meio)
                            
                            box_conteiner_principal.add_widget(box_info_frame_embaixo)
                            
                            
                            box_info_frame_encima.add_widget(icon)
                            box_info_frame_encima.add_widget(label_info_mercadoria)
                            
                            
                            box_info_frame_embaixo.add_widget(label_preco)
                            
                            box_info_frame_embaixo.add_widget(btn_add)
                            

                            
                            box_conteiner_principal.bind(minimum_height=box_conteiner_principal.setter("height"))
                            
                            box_info_frame_encima.bind(minimum_height=box_info_frame_encima.setter("height"))
                            
                            #box_frame_meio.bind(minimum_height=box_frame_meio.setter("height"))
                            
                            box_info_frame_embaixo.bind(minimum_height=box_info_frame_embaixo.setter("height"))
                            
                            
                        items.append((link_icon, link_icon2,icon, label_info_mercadoria, btn_add, merca))
                    self.pre_dowloads_icon(items)
                            
                            
                    
                #final da condição else --- >
                else:
                    box_pai.clear_widgets()
                    ima = Image(allow_stretch=True, size_hint=(1,None),source="icones/icon_sem_conexao/icon_sem_conexao.png", height=self.ids.box_merca_pai.height - dp(50))
                    with ima.canvas.before:
                        Color(1,11,1)
                        rect = RoundedRectangle(pos=ima.pos, size=ima.size, radius=[dp(100), 0, dp(100), 0], texture=self.app.criar_gradient_texture((1,0, 0, 1), (1, 0, 0,0.2), 150))
                    ima.bind(pos=lambda inst, value, rect=rect: setattr(rect, "pos", inst.pos), size=lambda inst, value, rect=rect: setattr(rect, "size", inst.size))
                    box_pai.add_widget(ima)
                    
                    popup = InfoGeral(arg=f"[color=#ff0000] [b](!)[/b] Erro ao acessar [b]Banco de dados[/b]!")
                    
                    
                    
                    
                    popup.open()
                # < -----
                
    
        
        # chamando icons das mercadorias --- >
                #th = threading.Thread(target=self.pre_dowloads_icon, args=(items,), daemon=True)
                #th.start()
                
                
    # < -------
            
            
        except Exception as erro:
            msg = erro
            self.app.gerenciamento_info_geral(f"(!) Erro em class: {__class__} > def organizar_mercadorias: {msg}\n{traceback.format_exc()}")
    
    
    
    
    
    def set_items(self, x):
        self.app.gerenciamento_info_geral(f" {x}")
        
        
        
        
        
    def add_carrinho(self, merca, info_preco, label_preco, cx_alterar_quant):
        cont_perso = int(cx_alterar_quant.text)
        
        if info_preco.upper() == "N/A":
            preco = info_preco
        else:
        
            preco = float(info_preco.replace(",", "."))
        
        
        if merca in self.lista_mercadoria_carrinho:
            
            
            self.lista_mercadoria_carrinho[merca]["quant"] +=cont_perso
            
            res = cont_perso * preco
            
            
            
            
            self.lista_mercadoria_carrinho[merca]["valor total"]  +=res
            
        else:
            self.lista_mercadoria_carrinho[merca] = {"quant": int(cx_alterar_quant.text), "valor uni": preco, "valor total": preco * cont_perso}
            

        if isinstance(self.lista_mercadoria_carrinho, dict):
            ultimos = list(self.lista_mercadoria_carrinho.items())[-5:]
            
            self.lista_merca_inverso = dict(ultimos[::-1])
        else:
            self.lista_merca_inverso = {}
            
        
        
        self.app.gerenciamento_info_geral(f"{self.lista_mercadoria_carrinho}\n\n [color=#00ff00]{self.lista_merca_inverso}")
        
        self.criar_items_carrinho(lista_items=self.lista_mercadoria_carrinho)
        
        self.construir_historico_compras(items=self.lista_merca_inverso)
        
        
        
        
        
    def construir_historico_compras(self, items):
        box =  self.ids.box_recentes_filho
        self.ids.scroll_recentes.scroll_x = 0
        if box:
            box.clear_widgets()
            
            for item, res_dict in items.items():
                btn = MDFillRoundFlatButton(text=f"{item}", size_hint=(None, None), size=(dp(100), dp(50)))
                box.add_widget(btn)
                #box.bind(minimum_size=box.setter("size"))
        
        
    def criar_items_carrinho(self, lista_items):
        cont = 0
        for item in lista_items:
            cont +=1
            self.cont_items_compras = cont
            self.ids.cont_items_carrinho.text = f"{self.cont_items_compras}"
            
        
        
        
        
    def pre_dowloads_icon(self, lista_mercadorias):
        
    
        for _ , (link, link2, icon, label, btn, merca) in enumerate(lista_mercadorias):
            
            self.downloads_icon(url=link, url2=link2, icon=icon, label=label, btn=btn, merca=merca)
            
            
        if hasattr(self, "pop") and self.pop:
            Clock.schedule_once(lambda dt:self.pop.dismiss(), 0.1)
        
        #resposta = requests.get(link_icon)
        
        
    def downloads_icon(self, url=None, url2=None, icon=None, label=None, btn=None, merca=None):
        local_root = primary_external_storage_path()
        local_icons= os.path.join(local_root, "win", "icons_mercadorias")
        
        if not os.path.exists(local_icons):
            os.makedirs(local_icons)
        
        
        
        safe = re.sub(r'[^-\w\. ]+', "_", str(merca or "sem_nome")).strip() or "sem_nome"
        nome_mercadoria_icon = f"{safe}.png"
        
        caminho_icon = os.path.join(local_icons, nome_mercadoria_icon)
        caminho_sem_media = os.path.join(local_icons, ".nomedia")
        if os.path.exists(caminho_sem_media):
            pass
        else:
            with open(caminho_sem_media, "w") as arq:
                pass
        
        
        
        
        
        def aplicar_existente(*_args, **_kwargs):
            def _ui(dt):
            
                if icon:
                    
                    icon.source = caminho_icon
                    icon.reload()
            Clock.schedule_once(_ui, 0)
                
                
                
                
        def aplicar_sem_foto(*_args, **kwargs):
            def _ui(dt):
                if icon:
                    icon.source = "icones/icon_sem_foto_frutas/icon_sem_foto_definida.png"
                    icon.reload()
            Clock.schedule_once(_ui, 0)
            
        if os.path.exists(caminho_icon):
            aplicar_existente()
            return
        
        
        if not (url or url2):
            aplicar_sem_foto()
            return
        
            
        req = UrlRequest(url= url2 if url2 else url, on_success=aplicar_existente, on_error=aplicar_sem_foto, on_failure=aplicar_sem_foto, file_path=caminho_icon, chunk_size=1024*64, timeout=30)
        
        
        
#< ---------