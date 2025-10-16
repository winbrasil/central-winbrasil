from bibliotecas import *

class Tab(MDBoxLayout, MDTabsBase):
    pass

class TelaOrdemServico(Screen):
    def __init__(self, **kwargs):
        self.date_picker = MDDatePicker()
        
        self.date_picker.bind(on_save=self.on_save)
        
        self.data_sistema = datetime.now().strftime("%d-%m-%y")
        
        self.app = MDApp.get_running_app()
        
        self.lista_clientes = []
        self.filtro_busca = ""
        
        super().__init__(**kwargs)
        
        
        
        
    def abrir_datepicker(self):
        self.date_picker.open()
        
        
    def on_save(self, instance, value, *a):
        self.data_escolhida_os = value.strftime("%d-%m-%y")
        Clock.schedule_once(lambda dt: self.organizador_widgets_items(), 0.05)
        
        
        
        
        
        
        

    
        
        
    def organizador_widgets_items(self):
        try:
            # Busca no banco os dados de ordem de serviço (OS)
            
            data_consulta = getattr(self,"data_escolhida_os", self.data_sistema)
            
            db_os = self.app.db_api.get("winbrasil",{}).get("empresas",{}).get("fpa",{}).get("os", {}).get(data_consulta, {})
            

                
            #self.app.gerenciamento_info_geral(lista_clientes_os_pendentes)
            texto_quant_pedido = self.ids.texto_quant_pedido
            cont_pedidos = 0
            
            lay_pendentes: MDBoxLayout=self.ids.box_items_pendentes
                
            lay_em_rota: MDBoxLayout=self.ids.box_items_em_rota
                
            lay_concluidos: MDBoxLayout=self.ids.box_items_concluidos
            # Verifica se db_os existe de fato
            
            
            data_pendentes = []
            data_em_rota = []
            data_concluido = []
            
            
            if db_os:
                
                
    
                # Percorre as OS pendentes
                # Percorre os clientes
                for cliente, dados_i in db_os.items():
                    status: str = dados_i.get("status", "N/A")

                    
                    
                    cont_pedidos +=1
                    
                    db_vendedor: dict = dados_i.get("vendedor", {})
                    
                    info_vendedor: str = db_vendedor.get("nome", "N/A")
                    
                    info_cor_vendedor = db_vendedor.get("cor", "[color=#0000ff] [b]")
                    
                    
                    db_info_pago = dados_i.get("info_pagamento", {})
                    
                    info_pagamento = db_info_pago.get("status", "N/A")
                    
                    info_cor_info_pag = db_info_pago.get("cor", "[color=#ff00ff]")
                    
                    items = {"data_str": data_consulta.replace("-", "/"), "cliente": cliente.upper(), "status": status.upper(), "vendedor": info_vendedor.upper(), "pagamento": info_pagamento, "info_cor_vendedor": info_cor_vendedor, "info_cor_pag": info_cor_info_pag}
                    
                    cop_status: str = status.strip().lower()
                    if cop_status == "pendente":
                            #self.ids.rv_pendentes.data = data_pendentes
                            data_pendentes.append(items)
                            
            
            
            
            

                            
                    if cop_status == "em rota":
                            #self.ids.rv_em_rota.data = data_em_rota
                            data_em_rota.append(items)
                            

                        
                    if cop_status =="concluido":
                            #self.ids.rv_concluidos.data = data_concluido
                            data_concluido.append(items)

                            
                    else:
                        pass
                        
                    
                        
                            
            else:
                pass
                
            
                
                
            def sem_dados_os(status: str=""):
                #return Label(text=" (!) Sem dados...")
                return {"data_str": f"{data_consulta.replace('-', '/')}", "cliente": "(!) Sem dados...", "status": "N/A", "vendedor": "N/A" }
            
            
            if not data_pendentes:
                data_pendentes = [sem_dados_os("pendentes")]
                
            if not data_em_rota:
                data_em_rota = [sem_dados_os("em rota")]
                
            if not data_concluido:
                data_concluido = [sem_dados_os("concluido")]
                
            self.ids.rv_pendentes.data = data_pendentes
            self.ids.rv_em_rota.data = data_em_rota
            self.ids.rv_concluidos.data = data_concluido
                
                
            texto_quant_pedido.text = f"Qt. Pedidos: {cont_pedidos:02d}"
    
        except Exception as erro:
            # Em caso de erro, manda log formatado para a função gerenciamento_info_geral
            tb = traceback.format_exc()
            msg_erro = erro
            Clock.schedule_once(lambda e=msg_erro, tb=tb:self.app.gerenciamento_info_geral(f"[color=#ff0000][b](!)[/b] [color=#ffff00]Erro em: {__name__} > \n traceback: [b]{tb}[/b] \n Exceção: [b]{e}\n {e.__class__}"))
            
            
            
            
            
            
            
            
            
            
class OSCard(MDCard):
    data_str = StringProperty("")
    cliente = StringProperty("")
    status = StringProperty("")
    vendedor = StringProperty("")
    pagamento = StringProperty("")
    info_cor_vendedor = StringProperty("")
    info_cor_pag = StringProperty("")