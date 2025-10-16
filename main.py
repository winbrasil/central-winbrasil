 # Importação de objetos ----------- >
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'system')

 
from kivy.compat import clock
from kivy.uix.progressbar import ProgressBar
from kivy.utils import platform
from kivy.app import App
from kivymd.app import MDApp
from kivy.base import Builder
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.clock  import  Clock
from functools import partial
from kivy.animation import  Animation
from kivy.uix.image import Image
import os


from kivymd.uix.button import *


if platform == 'android':
    from jnius import autoclass, cast
    from android.storage import app_storage_path
    from android.storage import primary_external_storage_path

from kivy.event import EventDispatcher

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, ShaderTransition, Translate, SwapTransition, FadeTransition, FallOutTransition, WipeTransition, RiseInTransition
from kivymd.uix.tab import MDTabs, MDTabsBase, MDTabsLabel
# < -------------------------------

#importacoes telas em py externo ---- >
from TelaVendas import TelaVendas
from TelaLogin import TelaLogin

from PreTelaLogin import PreTelaLogin
from TelaCadastramento import TelaCadastramento
from TelaPedido import TelaPedido
from TelaInicial import TelaInicial

from TelaCompras import TelaCompras

from TelaOrdemServico import TelaOrdemServico




# Importação dos layouts e widgets -------- >
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.effects.scroll import ScrollEffect


from kivy.uix.button import Button
from kivy.uix.label import Label
from  kivymd.uix.label  import MDLabel
from kivymd.uix.pickers import MDDatePicker
from  kivy.uix.textinput import TextInput

from kivymd.uix.spinner import MDSpinner

# < ----------------------------------

# Importação para trabalhar com gradientes 
from kivy.graphics.texture import Texture
from kivy.graphics import Color, Rectangle, RoundedRectangle, Ellipse, Line

# < ------------------------------

import socket
import requests
import traceback
import threading
from sseclient import  SSEClient
import json
import time
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
import asyncio
from kivy.storage.jsonstore import JsonStore



from datetime import datetime
#from kivymd.uix.pickers import MDDatePicker

from kivy.utils import get_color_from_hex
from kivy.core.audio import SoundLoader
#from kivy.uix.videoplayer import VideoPlayer
#from kivy.core.video import Video

import glob


class GerenciadorTelas(ScreenManager):
    pass



class AnimacaoTextos:
    def __init__(self, instance, duracao=1, repeticao=1, tempo=1, on_fim=None):
        self.instance = instance
        self.duracao = duracao
        self.repeticao = repeticao
        self.tempo = tempo
        self.on_fim = on_fim
        self.contador = 0
        self.animacao_ativa = True

        self.instance.opacity = 0
        self.fade_in()
        #self.bind(on_complete=lambda dt: setattr(self, "instance", 1))


    def fade_in(self):
        if not self.animacao_ativa:
            #self.instance.opacity = 1
            return

        anim = Animation(opacity=1, duration=self.duracao)
        anim.bind(on_complete=lambda *a: Clock.schedule_once(lambda dt: self.fade_out(), self.tempo) )
        anim.start(self.instance)

    def fade_out(self):
        
        if not self.animacao_ativa:
            #self.instance.opacity = 1
            return

        anim = Animation(opacity=0, duration=self.duracao)
        anim.bind(on_complete=lambda dt, *a: Clock.schedule_once(lambda dt, *a: self.repetir_ou_encerrar(anim=anim)))
        anim.start(self.instance)

    def repetir_ou_encerrar(self, anim, *args):
        self.contador += 1
        if self.contador < self.repeticao:
            Clock.schedule_once(lambda dt, *a: self.fade_in(), self.tempo)
        else:
            self.instance.opacity = 1  # Garante visibilidade final
            if self.on_fim:
                Clock.schedule_once(lambda dt, *a: self.on_fim(), self.tempo)

                
                #anim.bind(on_complete=lambda *a: Clock.schedule_once(lambda *a: setattr(self.instance, "opacity", 1)))

    def parar_animacao(self):
        self.animacao_ativa = False
        Animation.cancel_all(self.instance)
        #self.instance.opacity = 1


        


class InfoGeral(Popup):
    def __init__(self, arg="", modo="",tempo=None, **kwargs):
        self.index_textos = 0
        self.tempo = tempo
        self.arg = arg
        self.app = MDApp.get_running_app()

        super().__init__(**kwargs)
        
        #Configuração Popup/info_geral -------- >
        self.size_hint = (None, None)
        self.separator_height = 0
        self.title = ""
        self.background_color = (0.2,0,1,0)
        self.title_size = 0
        self.arg = arg
        self.modo = modo


        
        #self.background = "popup_icon.jpg"
        #self.border = [dp(0.1), dp(0.2), dp(0.1), dp(0.01)]
        
        
        
        #< -----------------------------------
        
        
        
        self.conteiner_primario = BoxLayout(orientation="vertical")
        
        self.spinner = MDSpinner(size_hint=(None, None), size=(dp(30), dp(30)), pos_hint={"center_x":0.5})
        
        
        self.content= self.conteiner_primario
        
        self.conteiner_segundario = BoxLayout(orientation="vertical")
        
        self.conteiner_primario.add_widget(self.conteiner_segundario)
        
        self.conteiner_terceiro = BoxLayout(orientation="vertical", size_hint=(1, None), spacing=dp(5), padding=dp(10))
        
        with self.canvas.before:
            self.rect = Rectangle(pos=self.pos, size=self.size, texture=self.app.criar_gradient_texture())
            Color(1, 1, 1, 1)
            linha = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(10)), width=dp(0.5))
        self.bind(size=self.atua_canvas, pos=self.atua_canvas)
            
        
        # Atualiza a linha diretamente com lambda e setattr:
        self.bind(
            pos=lambda instance, value: setattr(linha, "rounded_rectangle", (self.x, self.y, self.width, self.height, dp(10))),
            size=lambda instance, value: setattr(linha, "rounded_rectangle", (self.x, self.y, self.width, self.height, dp(10)))
        )
        

                
        self.scrollview_conteiner_segundario = ScrollView(bar_width=0, do_scroll_x=False)
        
        
        self.texto_info_geral = Label(markup=True, text=self.arg if modo != "carregamento" else "carregamento ...", halign="center", valign="middle", size_hint=(None,None), text_size=(Window.width *0.8, None), opacity=0, font_name="fonte/Passion_One/PassionOne-Regular.ttf", font_size=sp(20), width=Window.width * 0.75)
        
        self.texto_info_geral.bind(texture_size=self.atua_tam_fonte)
        
        self.texto_info_geral.bind(
    text=lambda *args: Clock.schedule_once(self.atua_tam_fonte, 0)
)        
        self.conteiner_terceiro.add_widget(self.texto_info_geral)
        
        if modo == "carregamento":
            #self.texto_info_geral.size_hint_x = 1
            self.conteiner_terceiro.orientation = "vertical"
            
            self.conteiner_terceiro.add_widget(self.spinner)
        
        
        self.conteiner_segundario.add_widget(self.scrollview_conteiner_segundario)
        
        self.scrollview_conteiner_segundario.add_widget(self.conteiner_terceiro)
               
        
        AnimacaoTextos(instance=self.texto_info_geral, duracao=2)
        
                
    def chamar_animacao_info_geral(self):
        if hasattr(self, "parar_cont_index"):
            self.parar_cont_index.cancel()
    
        self.texto_info_geral.text = ""
        self.index_textos = 0
    
        self.parar_cont_index = Clock.schedule_interval(self.movimentacao_textos, 0.01)


        
    def movimentacao_textos(self, dt=None):
        if self.index_textos < len(self.arg):
            self.texto_info_geral.text = self.arg[:self.index_textos+1]
            self.index_textos += 1
        else:
            self.index_textos = 0
            self.parar_cont_index.cancel()

            
# Configuração da fonte dos widgtes popup -- >
    def atua_tam_fonte(self, *args):
        self.texto_info_geral.texture_update()
    
        altura_label = self.texto_info_geral.texture_size[1]
        largura_label = self.texto_info_geral.texture_size[0]
    
        self.texto_info_geral.height = altura_label 
        self.conteiner_terceiro.height = altura_label + dp(40)
    
        largura = largura_label + dp(80)
        altura = altura_label + dp(100)
    
        largura = min(largura, Window.width * 0.9)
        altura = min(altura , Window.height * 0.8)
    
        self.size = (largura, altura)
        self.conteiner_primario.size = (largura, altura)
        self.content.size = (largura, altura)
        
        
        
        
    def atua_canvas(self, *args):
               self.rect.pos = self.pos
               self.rect.size = self.size
               
#< ----------------------

class PreTelaInicial(Screen):
    def __init__(self, db, **kwargs):
        
        self.fonte_padrao = MDApp.get_running_app().fonte_padrao
        self.app = MDApp.get_running_app()
        
        self.db_api = db
        self.cont_tentativas_conexao = 0
        
        super().__init__(**kwargs)
        

    def on_enter(self):
        app = MDApp.get_running_app()
        self.db_api = app.db_api
        self.texto_saudacao = self.ids.texto_saudacao
        self.texto_saudacao.text = ""
        msg = self.app.root.get_screen("tela_login").login_firebase(email="permissao.temporaria@gmail.com", senha="510897")
        
        self.by = self.ids.btn_id
        #AnimacaoTextos(instance=self.by, duracao=2)
        
        #AnimacaoTextos(instance=self.texto_saudacao, duracao=3, repeticao=1)
    
        self.index = 0
        
        
        texto = self.db_api.get("winbrasil", {}).get("telas", {}).get("pre_tela_inicial", {}).get("texto_saudacao")

        
        self.texto_animado = texto if texto else "Aguarde ..."


        
        
        self.tempo_atual = 0.02
        self.delta = -0.3
    
        Clock.schedule_once(self.animar_texto_saudacao, self.tempo_atual)
        
        
        
    


    def animar_texto_saudacao(self, dt):
        if self.index < len(self.texto_animado):
            self.texto_saudacao.text = self.texto_animado[:self.index + 1]
            self.index += 1
    
            # alterna entre acelerar e desacelerar
            if self.tempo_atual <= 0.02:
                self.delta = 0.005
            elif self.tempo_atual >= 0.2:
                self.delta = -0.3
    
            self.tempo_atual += self.delta
            
            Clock.schedule_once(self.animar_texto_saudacao, self.tempo_atual)
            
            
        else:
            #app = MDApp.get_running_app()
            #self.db_api = app.db_api
            self.index = 0
            if self.db_api:
#chamando os botões sair e iniciar da class pre_tela_inicial ------------ >


                AnimacaoTextos(instance=self.ids.btn_pre_iniciar, duracao=2)
                AnimacaoTextos(instance=self.ids.prosseguir, duracao=2)
                
                self.cont_tentativas_conexao = 0
            else:
                self.cont_tentativas_conexao +=1
                #self.texto_saudacao = ""
                Clock.schedule_once(lambda dt:self.on_enter(),self.cont_tentativas_conexao)
                self.cont_tentativas_conexao = 0


# <-------------------------        
            
    def sair(self): 
            app = MDApp.get_running_app()
            tela_sair = app.root.get_screen("tela_sair")
            tela_sair.cod_geral(tela=app.root.current, k=27, window=None)
            #Sair(encaminhamento_btn=True)
            

class Sair(Screen):
    def __init__(self, encaminhamento_btn, **kwargs):
        self.cont_sair = 3
        self.resetar_cont_sair = None
        self.cont_tela = 0
        self.historico_telas = ["tela_inicial"]  # Guarda sequência de telas visitadas
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)

        if encaminhamento_btn:
            Clock.schedule_once(lambda dt: self.cod_geral(tela=self.app.root.current, k=27, window=None), 0)

        Window.bind(on_keyboard=lambda win, k, *args: self.cod_geral(tela=self.app.root.current, k=k, window=win))

    def cod_geral(self, tela, window, k):
        
        
        app = MDApp.get_running_app()

        sm = app.root
        self.registrar_tela(sm.current)
        
        #InfoGeral(arg=str(self.historico_telas)).open()
        #return True
        if k == 27:

            if sm.current =="tela_inicial":
                self.cont_sair -=1
                
                InfoGeral(arg=f" • Click mais {self.cont_sair} para sair. ").open()
                if self.cont_sair <=0:
                    icons = os.path.join(primary_external_storage_path(), "win", "icons_mercadorias")
                    
                    if os.path.exists(icons):
                        for caminho in glob.glob(os.path.join(icons, "*png")):
                            os.remove(caminho)
                    app.stop()

                if self.resetar_cont_sair is None:
                    Clock.schedule_once(self.resetar_cont_sair_callback, 5)
                    
                    
                    
                
                    self.resetar_cont_sair = True
                return True
                
            else:
                if sm.current =="previa_tela_inicial":
                    return True
                    
                else:
                    if self.historico_telas:
                        nova_tela = self.historico_telas[-1]
                        sm.current = nova_tela
                    
                    return True
                    
                return False
                        
                        
                        
                        
    def registrar_tela(self, nome_tela):
        try:
            if nome_tela in ("tela_login", "tela_cadastramento"):
                return 
            if not self.historico_telas or self.historico_telas[-1] != nome_tela:
                self.historico_telas.append(nome_tela)
                    
            else:
                self.historico_telas.pop()
                
        except Exception as erro:
            msg_erro = erro
            self.app.gerenciamento_info_geral(msg_erro)
            
            
            
    def resetar_cont_sair_callback(self, dt):
        self.cont_sair = 3
        self.resetar_cont_sair = None

        
                    
            
            
class PreviaTelaInicial(Screen):
    def __init__(self,encaminhamento="", **kwargs):
        self.encaminhamento = encaminhamento
        super().__init__(**kwargs)
        
        #self.texto_apresentacao = ""
        self.labels = []
        self.esperar_troca_tela = 0
        
        
    def on_enter(self):
        Clock.schedule_once(lambda dt: self.criar_letras(), 0.1)
        self.parar_tempo_tela = Clock.schedule_interval(lambda dt:self.tempo_tela(), 1)
        
        
        
        
    def criar_letras(self):
        app = MDApp.get_running_app()
        self.db_api = app.db_api
        previa_tela_inicial = self.db_api.get("telas", {}).get("previa_tela_inicial", {}).get("texto", {}) if self.db_api.get("telas", {}).get("previa_tela_inicial", {}).get("texto") else "WINBRASIL"
        espacamento = 0.08
        
        posx = 0.15
        for letras in previa_tela_inicial:
            label = Label(markup=True, text=f"[i]{letras}", size_hint=(None, None), pos_hint={"x":posx, "y":0},font_size=(MDApp.get_running_app().fonte_padrao*1.1), opacity=0, font_name="fonte/Rubik_Mono_One/RubikMonoOne-Regular.ttf")
            #label.size = label.texture_size
            
            self.ids.conteiner_primario.add_widget(label)
            self.labels.append(label)
            posx +=espacamento
            
            with label.canvas.before:
                rect = RoundedRectangle(pos=label.pos, size=label.size, texture=app.criar_gradient_texture(), radius=[dp(20)])
            label.bind(size=lambda instance, value, rect=rect: (
        setattr(rect, "size", instance.texture_size),
        setattr(rect, "texture", app.criar_gradient_texture())
    ),
    pos=lambda instance, value, rect=rect: (
        setattr(rect, "pos", instance.pos),
        setattr(rect, "texture", app.criar_gradient_texture())
    )
)

                    
                    
            Clock.schedule_once(lambda dt: self.animar_letras(), 0)
        
        
        
    def animar_letras(self):
        for i, label in enumerate(self.labels):
            delay = i * 0.1
                
            Clock.schedule_once(lambda dt, lbl =label: self.animar_label(label=lbl), delay)
                
    def animar_label(self, label):
        anima = Animation(pos_hint={"x":label.pos_hint["x"], "y":0.5}, opacity=1, duration=0.1) + \
            Animation(opacity=0.2, duration=0.6) + \
            Animation(opacity=1, duration=0.6)
            
        anima.repeat = True
        anima.start(label)
        
        
            
    def tempo_tela(self):
        self.esperar_troca_tela +=1
        if self.esperar_troca_tela >=3:
            setattr(MDApp.get_running_app().root, "current", self.encaminhamento)
            self.esperar_troca_tela = 0
            self.parar_tempo_tela.cancel()
            
            
            
            
            
                        
            
            
            
        

            
            
            
            
            
            
            
            
            
            
class MeuApp(MDApp):
    tamanho_x_tela = Window.width
    tamanho_y_tela = Window.height
    
    def __init__(self, **kwargs):
  
        
        self.status_conexao_internet = None
        self.cont_reconexao = 0
        self.reconexao = False
        self.usuario_verificado = None
        self.mercadoria_destino = None
        self.classe_java()
        self.window = Window
        self.versao_nome = "0.1"
        self.permissao_temporaria_login = None
        self.api_key = "AIzaSyATicQTeRmBrWIHmNIzoi5zL3w-Lo7PkAw"       
        
        super().__init__(**kwargs)
        
        self.info_geral_build = InfoGeral()
        
        self.permissao_manager()
        self.obter_versao_sdk()
        
        Clock.schedule_once(lambda dt:self.verificacao_permissioes(), 1)
        
        self.login_usuario = None
        self.usuario_logado_email = None
        self.id_token = None
        self.usuario_uid = None


# def responsável pelos downloads, como de atualização do próprio aplicativo --- >
    def downloads_atualizacao(self, url: str = None, destino_memoria: str = None,widget: Button = None, barra_progresso: ProgressBar = None,tipo=None, permissao: str = None):
        
        
        
        try:
            req = requests.get(url, stream=True, timeout=60)
            if req.status_code != 200:
                Clock.schedule_once(lambda dt: InfoGeral(arg=f'(!) Erro ao tentar baixar{f" {tipo}" if tipo else ""}: {req.status_code}').open())
                return

            pasta = destino_memoria or self.memoria_android_privado()
            os.makedirs(pasta, exist_ok=True)

            caminho_zip = os.path.join(pasta, 'base.zip')
            caminho_apk_antigo = os.path.join(pasta, 'base.apk')
            if os.path.exists(caminho_apk_antigo):
                try:
                    os.remove(caminho_apk_antigo)  # remove corretamente
                except:
                    pass

            total = int(req.headers.get('content-length', 0))
            baixado = 0

            with open(caminho_zip, permissao if permissao else 'wb') as f:
                for chunk in req.iter_content(chunk_size=1024 * 64):
                    if not chunk:
                        continue
                    f.write(chunk)

                    if total > 0:
                        baixado += len(chunk)
                        p = int((baixado / total) * 100)
                        Clock.schedule_once(lambda dt, p=p: (
                            barra_progresso and setattr(barra_progresso, 'value', p),widget and setattr(widget, 'text', f'{p}%')))
                    else:
                        # Sem content-length → feedback suave
                        Clock.schedule_once(lambda dt: (
                            barra_progresso and setattr(barra_progresso, 'value',
                                                        min(99, (barra_progresso.value if barra_progresso else 0) + 1)),
                            widget and setattr(widget, 'text',
                                               f'{int(barra_progresso.value) if barra_progresso else 0}%')
                        ))

            # Finaliza UI
            Clock.schedule_once(lambda dt: (
                barra_progresso and setattr(barra_progresso, 'value', 100), widget and setattr(widget, 'text', '100%')))

            # chama descompactar com os argumentos corretos
            Clock.schedule_once(lambda dt: self.descompactar(caminho_zip=caminho_zip, pasta_destino=pasta))

        except Exception as e:
            Clock.schedule_once(lambda dt, erro=e: InfoGeral(arg=f'(!) Exceção em downloads_atualizacao:\n{erro}').open())

    #< -------------------------

    def descompactar(self, caminho_zip: str, pasta_destino: str) -> str:
        """
        Espera um ZIP com um único arquivo (APK).
        Extrai para 'pasta_destino', apaga o ZIP e chama instalar_apk.
        """
        try:
            if not os.path.exists(caminho_zip):
                Clock.schedule_once(lambda dt: self.gerenciamento_info_geral(f"[color=#ff0000]ZIP não encontrado:\n{caminho_zip}"))
                return ""

            if not zipfile.is_zipfile(caminho_zip):
                Clock.schedule_once(lambda dt: self.gerenciamento_info_geral("[color=#ff0000]Arquivo não é um ZIP válido"))
                return ""

            os.makedirs(pasta_destino, exist_ok=True)

            with zipfile.ZipFile(caminho_zip, "r") as z:
                z.extractall(pasta_destino)
                # pega apenas arquivos (ignora diretórios)
                nomes = [n for n in z.namelist() if not n.endswith('/')]
                if not nomes:
                    Clock.schedule_once(lambda dt: self.gerenciamento_info_geral(
                        "[color=#ff0000]ZIP extraído, mas estava vazio"))
                    return ""
                nome_no_zip = nomes[0]

            # move para a raiz se veio em subpasta
            extraido = os.path.join(pasta_destino, nome_no_zip)
            caminho_apk = os.path.join(pasta_destino, os.path.basename(nome_no_zip))
            if extraido != caminho_apk and os.path.exists(extraido):
                os.replace(extraido, caminho_apk)

            # apaga o ZIP
            try:
                os.remove(caminho_zip)
            except:
                pass

            # instala ao terminar (UI thread)
            Clock.schedule_once(lambda dt, p=caminho_apk: self.instalar_apk(p))
            return caminho_apk

        except Exception as e:
            Clock.schedule_once(lambda dt: self.gerenciamento_info_geral(
                f"[color=#ff0000]Erro ao descompactar/instalar:\n{e}"))
            return ""

    def instalar_apk(self, caminho_apk: str) -> None:
        try:
            if platform != "android":
                self.gerenciamento_info_geral("Instalação disponível só no Android.")
                return

            # Android 8+ → garantir permissão de instalar de fontes desconhecidas
            if self.BuildVersion.SDK_INT >= 26:
                pm = self.context.getPackageManager()
                if not pm.canRequestPackageInstalls():
                    self.permissao_fonte_desconhecida()
                    self.gerenciamento_info_geral("[color=#ffff00]Ative 'Permitir desta fonte' e tente novamente.")
                    return

            File = autoclass("java.io.File")
            Intent = self.Intent
            Uri = self.Uri

            apk_file = File(caminho_apk)

            if self.BuildVersion.SDK_INT >= 24:
                # Android 7+ → FileProvider (content://)
                FileProvider = autoclass("androidx.core.content.FileProvider")
                authority = self.context.getPackageName() + ".fileprovider"
                uri = FileProvider.getUriForFile(self.activity, authority, apk_file)

                intent = Intent(Intent.ACTION_VIEW)
                intent.setDataAndType(uri, "application/vnd.android.package-archive")
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            else:
                # Android 6 ou anterior → file://
                uri = Uri.fromFile(apk_file)
                intent = Intent(Intent.ACTION_VIEW)
                intent.setDataAndType(uri, "application/vnd.android.package-archive")
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)

            self.activity.startActivity(intent)

        except Exception as e:
            Clock.schedule_once(lambda dt: self.gerenciamento_info_geral(
                f"[color=#ff0000]Erro ao iniciar instalação:\n{e}"))

    def obter_versao_sdk(self):
        try:

            if platform =="android":
                package_manager = self.activity.getPackageManager()
                package_name = self.activity.getPackageName()
                package_info = package_manager.getPackageInfo(package_name, 0)
                
                self.versao_nome = package_info.versionName
                
                if self.BuildVersion.SDK_INT >=28:
                    self.versao_code_android_superior = package_info.getLongVersionCode()
                    
                    return self.versao_nome, self.versao_code_android_superior
                else:
                    versao_code = package_info.versionCode
                    return self.versao_nome, versao_code
                    
                
            
        except Exception as erro:
            msg_erro = erro
            
            return False, self.gerenciamento_info_geral(msg=msg_erro)
            
            
    def memoria_android_legivel_usuario(self) -> str:
        '''memória do android que usuario pode ter acesso/pasta android da raiz'''
        memoria_android_publica = self.activity.getExternalFilesDir(None)
        return os.path.join(memoria_android_publica.getAbsolutePath())

    def memoria_android_privado(self):
        '''memória inacessivél ao usuário'''
        memoria_privada_android = app_storage_path()
        return memoria_privada_android


    def classe_java(self):
        try:
            if platform !="android":
                return
            self.PythonActivity = autoclass("org.kivy.android.PythonActivity")
            self.BuildVersion = autoclass("android.os.Build$VERSION")
            self.Settings = autoclass("android.provider.Settings")
            self.Uri = autoclass("android.net.Uri")
            self.Intent = autoclass("android.content.Intent")

            self.Context = autoclass("android.content.Context")
            self.Build = autoclass("android.os.Build")
            self.PackageManager = autoclass("android.content.pm.PackageManager")
            
            
            
            self.activity = self.PythonActivity.mActivity
            
            
            self.context = cast("android.content.Context", self.activity)
            
        except Exception as erro:
            msg_erro = erro
            self.gerenciamento_info_geral(msg=msg_erro)
        
        
        
    def permissao_manager(self):
        try:
            if platform != "android":
                return 
            if self.BuildVersion.SDK_INT >=30:
                Environment = autoclass("android.os.Environment")
                if not Environment.isExternalStorageManager():
                    intent = self.Intent(self.Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION)
                    uri = self.Uri.parse("package:"+ self.context.getPackageName())
                    
                    intent.setData(uri)
                    self.activity.startActivity(intent)
            
            
        except Exception as erro:
            msg_erro = erro
            self.gerenciamento_info_geral(msg=msg_erro)
            
            
    def permissao_fonte_desconhecida(self):
        try:
            if platform != "android":
                return
            if self.BuildVersion.SDK_INT >= 26:
                if not self.context.getPackageManager().canRequestPackageInstalls():
                    uri = self.Uri.parse("package:" + self.context.getPackageName())
                    intent = self.Intent(self.Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES, uri)
                    intent.setFlags(self.Intent.FLAG_ACTIVITY_NEW_TASK)
                    self.tempo_saida_permissao = time.time()
                    self.activity.startActivity(intent)
            else:
                # Android 7 ou inferior
                intent = self.Intent(self.Settings.ACTION_SECURITY_SETTINGS)
                intent.setFlags(self.Intent.FLAG_ACTIVITY_NEW_TASK)
                self.tempo_saida_permissao = time.time()
                self.activity.startActivity(intent)
        except Exception as erro:
            msg_erro = erro
            self.gerenciamento_info_geral(msg=msg_erro)
    
            
    def on_resume(self):
        if hasattr(self, "tempo_saida_permissao"):
            tempo_volta = time.time() - self.tempo_saida_permissao
            if tempo_volta >= 10:
                self.gerenciamento_info_geral("[color=00ff00]Usuário provavelmente autorizou a instalação de fontes desconhecidas.")
            else:
                self.gerenciamento_info_geral("[color=ff0000]Usuário voltou antes de 10s. Talvez não autorizou.")
            del self.tempo_saida_permissao
        
            
                
            
        
    def verificacao_permissioes(self):
        try:
            if platform == "android":
                from android.permissions import Permission, request_permissions, check_permission
                
                
                permissões_necessarias = [Permission.POST_NOTIFICATIONS, Permission.FOREGROUND_SERVICE, Permission.READ_EXTERNAL_STORAGE, Permission.WAKE_LOCK, Permission.WRITE_EXTERNAL_STORAGE, Permission.ACCESS_NETWORK_STATE, Permission.REQUEST_INSTALL_PACKAGES]
                
                permissoes_faltando = [p for p in permissões_necessarias if not check_permission(p)]
                
                if permissoes_faltando:
                    request_permissions(permissoes_faltando)

            
                
        except Exception as erro:
            msg_erro = f"[b][color=#ff0000](!) [/b][i]Erro nas permissiões, em [color=ff00ff][u]def verificar_permissiões[/u]. [color=#ffff00]\nErro: {erro}\n{erro.__class__}"
            self.gerenciamento_info_geral(msg_erro)


    def gerenciamento_info_geral(self, msg):
        try:
            self.info_geral_build.texto_info_geral.text = str(msg)
            self.info_geral_build.texto_info_geral.texture_update()
            self.info_geral_build.atua_tam_fonte()
            self.info_geral_build.open()
            
        except Exception as erro:
            msg_erro = erro
            popup = InfoGeral(arg=str(erro))
            popup.open()
            
            
        
            
    def verificar_token(self, id_token, novo_token=None):
        try:
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={self.api_key}"
            resposta = requests.post(url=url, json={"idToken": id_token})
            dados = resposta.json()
            if resposta.status_code ==200:
                Clock.schedule_once(lambda dt: self.info_geral_build.dismiss(),  4)
                
                Clock.schedule_once(lambda dt: (self.gerenciamento_info_geral(f"Chave token válida, [color=#00ff00]{resposta.status_code} ok")), 5)
                
                Clock.schedule_once(lambda dt: self.info_geral_build.dismiss(),  7)
                
                
                Clock.schedule_once(lambda dt: setattr(self, "permissao_temporaria_login", True))
                
                
                #Clock.schedule_once(lambda dt:setattr(self, "usuario_verificado", True),0)
                
                th = threading.Thread(target=self.db, daemon=True)
                th.start()
                return True
                

                
            else:
                
                Clock.schedule_once(lambda dt: setattr(self, "permissao_temporaria_login", None))
                #Clock.schedule_once(lambda dt:setattr(self, "usuario_verificado", None),0)
                
                if novo_token:

                
                    th =  threading.Thread(target=lambda:self.renovar_token(refresh=self.refreshToken), daemon=True)
                    th.start()
                    
                    
                    
                    
                    
        except Exception as erro:
            msg = erro
            Clock.schedule_once(lambda dt: self.gerenciamento_info_geral(f"Erro em class: {__class__} def verificar_token: {msg}\n[color=#ffff00]{traceback.format_exc()}"))
            
            
            
                        
            
    def renovar_token(self, refresh):
        try:
            if refresh:
                url = f"https://securetoken.googleapis.com/v1/token?key={self.api_key}"
                resposta = requests.post(url=url, data={"grant_type": "refresh_token", "refresh_token":refresh})
                dados = resposta.json()
                if resposta.status_code ==200:
                    self.id_token  = dados.get("id_token")
                    self.refreshToken = dados.get("refresh_token", refresh)
                    
                    self.login_usuario.put("auth", token=self.id_token, refreshToken=self.refreshToken,email=self.usuario_logado_email, uid=self.usuario_uid)
                    
                    #Clock.schedule_once(lambda dt:setattr(self, "permissao_temporaria_login", True),0)
                    
                    
                    #Clock.schedule_once(lambda dt:setattr(self, "usuario_verificado", True),0)
                    th = threading.Thread(target=lambda: self.verificar_token(id_token=self.id_token), daemon=True)
                    th.start()
                    
                    
        
    
                    
                    Clock.schedule_once(lambda dt: InfoGeral(arg=f"[color=#00ff00]Info: def renovar_token\nToken renovado com sucesso!").open(), 1)
                    #th = threading.Thread(target=self.db, daemon=True)
                    #th.start()
                    return True
                    
                else:
                    erro = dados.get("error", {}).get("message")
                    if erro == "USER_DISABLED":
                        Clock.schedule_once(lambda dt:InfoGeral(arg=f"[color=#ff0000]Impossível obter token de acesso.\n [color=#ffff00][i]Usuário desativado![/i][/color]").open(), 3)
                        Clock.schedule_once(lambda dt: self.info_geral_build.dismiss(), 3)
                    
                    Clock.schedule_once(lambda dt:setattr(self, "permissao_temporaria_login", None),0)
                    Clock.schedule_once(lambda dt:setattr(self, "usuario_verificado", None),0)
                    
                    
                    return False


#caso refresh seja none --------- >
            else:
                Clock.schedule_once(lambda dt:InfoGeral(arg=f"Impossível obter token. Faça login ou cadastro!\n Refresh: {refresh}").open(), 25)
                Clock.schedule_once(lambda dt:setattr(self, "permissao_temporaria_login", None),0)
                Clock.schedule_once(lambda dt:setattr(self, "usuario_verificado", None),0)
                
                
                return False, f"Erro na class: {__class__} > def renovar token, ao obter refresh: {refresh}"
# < --------------
        except Exception as erro:
            msg = erro
            return False, Clock.schedule_once(lambda dt: self.gerenciamento_info_geral(f"Erro em class: {__class__} def verificar_token: {msg}\n[color=#ffff00]{traceback.format_exc()}"))
        

        
              
            
    def on_start(self):
        try:
            if self.login_usuario:
                if self.login_usuario.exists("auth"):
                    dados = self.login_usuario.get("auth")
                    self.id_token = dados.get("token")
                    
                    self.usuario_logado_email = dados.get("email")
                    self.usuario_uid = dados.get("uid")
                    
                    self.refreshToken = dados.get("refreshToken")
                    
                    setattr(self, "permissao_temporaria_login", True)
                    
                    setattr(self, "usuario_verificado", True)
                    
                    th_verificacao_token = threading.Thread(target=lambda:self.verificar_token(id_token=self.id_token, novo_token=True), daemon=True)
                    th_verificacao_token.start()
                    
                    
                else:
                    Clock.schedule_once(lambda dt:InfoGeral("Info em on_start: auth não existe em usuário login!").open())
                    self.usuario_verificado = None
                    
                    
            else:
                pass
                #Clock.schedule_once(lambda dt:setattr(self.root, "current" ,"pre_tela_login"), 0)
                
                
                
        except Exception as erro:
            msg = erro
            self.gerenciamento_info_geral(msg=f"Erro na class: {__class__} > def on_start: {msg}\n[color=#ffff00]{traceback.format_exc()}")
            
      
    def build(self):
        try:
            
            
            Window.softinput_mode = "below_target"
            
            Builder.load_file("pre_tela_inicial.kv")
            Builder.load_file("tela_inicial.kv")
            Builder.load_file("previa_tela_inicial.kv")
            Builder.load_file("tela_cadastramento.kv")
            Builder.load_file("tela_login.kv")
            Builder.load_file("tela_vendas.kv")
            Builder.load_file("pre_tela_login.kv")
            Builder.load_file("tela_pedido.kv")
            Builder.load_file("tela_compras.kv")
            Builder.load_file("tela_os.kv")
            
            
            self.link_api = "https://empresarial-a22dd-default-rtdb.firebaseio.com/"
            
            self.db_api = {}
#            
            caminho_android = os.path.join(app_storage_path(), "login_usuario.json")
            
#
            caminho_json = os.path.join(caminho_android)
#
            

            sm = GerenciadorTelas()
            self.root = sm
            
            
    
            self.fonte_padrao = self.tamanho_x_tela *0.05 + self.tamanho_y_tela *0.01
            
            self.tela_compras = TelaCompras(name="tela_compras")
            
            self.pre_tela_login = PreTelaLogin(name="pre_tela_login")
            
            self.tela_login = TelaLogin(name="tela_login")
            
            self.tela_os = TelaOrdemServico(name="tela_os")
            
            
            self.pre_tela_inicial = PreTelaInicial(name="pre_tela_inicial", db=self.db_api)
            
            self.previa_tela_inicial = PreviaTelaInicial(name="previa_tela_inicial")
            
            self.tela_pedido = TelaPedido(name="tela_pedido")
            
            
            
            self.tela_inicial = TelaInicial(name="tela_inicial")
            
            self.tela_cadastramento = TelaCadastramento(name="tela_cadastramento")
            #self.tela_codigo_verificacao = Autenticacao(name="tela_codigo_verificacao")
            
            
            
            self.tela_vendas = TelaVendas(name="tela_vendas")
            
            
            #self.root = sm
            tela_sair = Sair(name="tela_sair", encaminhamento_btn=False)
            sm.add_widget(tela_sair)
            
            
            sm.add_widget(self.previa_tela_inicial)
            sm.add_widget(self.pre_tela_login)
            #sm.add_widget(self.pre_tela_inicial)
            sm.add_widget(self.tela_compras)
            
            sm.add_widget(self.tela_inicial)
            sm.add_widget(self.tela_cadastramento)

            
            sm.add_widget(self.tela_vendas)
            
            sm.add_widget(self.tela_os)
            
            sm.add_widget(self.tela_login)
            sm.add_widget(self.tela_pedido)
            sm.add_widget(self.pre_tela_inicial)
            
            self.login_usuario = JsonStore(caminho_json)
            
            
            
            
            
            if platform !="android":
                sm.current ="tela_inicial"
                return sm
            
            caminho_root = primary_external_storage_path() + "/win"
            caminho_arquivo = os.path.join(caminho_root, "config.text")
            
            
            
            if not  os.path.exists(caminho_root):
                self.permissao_fonte_desconhecida()
                os.makedirs(caminho_root)
    
            if not os.path.exists(caminho_arquivo):
                pass
                
                #with open(caminho_arquivo, "w") as f:
                    #f.write("Primeiro acesso: True")
                self.previa_tela_inicial.encaminhamento= "pre_tela_inicial"
                Clock.schedule_once(lambda dt: setattr(sm, "current", "previa_tela_inicial"), 0.1)
            else:
                self.previa_tela_inicial.encaminhamento="tela_inicial"
                Clock.schedule_once(lambda dt: setattr(sm, "current", "previa_tela_inicial"), 0)
                       
            sm.transition = FadeTransition(duration=0.5)
            
            
            
            
            
                
            return sm
                     
        except Exception as erro:
            msg_erro = erro
            self.gerenciamento_info_geral(msg=f"[color=#ff0000](!) {msg_erro}\n[color=#ffff00]{traceback.format_exc()}")
        

    def criar_gradient_texture(self, cor_inicial=(0,0.5 ,0.2,1), cor_final=(1,1 ,1 ,0.4), alpha=255):
        
        # Cria textura de 1px de largura e 64px de altura ------- >
        height = Window.height
        width = Window.width
        texture = Texture.create(size=(1, 63), colorfmt="rgba")
        # < ------------
        
        
        #Ativa modo de escrita manual ----- >
        #texture.bind()
        buf = []
        for i in range(63):
            t = i /63
            r = int((cor_inicial[0] + (cor_final[0] - cor_inicial[0]) *t) * alpha)
            
            g = int((cor_inicial[1] + (cor_final[1] - cor_inicial[1]) *t) * alpha)
            
            b = int((cor_inicial[2] + (cor_final[2] - cor_inicial[2]) *t) * alpha)
            
            a = int((cor_inicial[3] + (cor_final[3] - cor_inicial[3]) *t) * alpha)
            
            
            buf.extend([r, g, b, a])
        buf = bytes(buf)
        texture.blit_buffer(buf, colorfmt="rgba", bufferfmt="ubyte")
        texture.wrap = "repeat"
        #texture.uvsize = (-1, 1)
        return texture
        
# Banco de Dados  ----------------- >        
    def db(self):
        while True:
            try:
                if self.permissao_temporaria_login is None:
                    #break
                    time.sleep(5)
                    continue
                    
                sseclient = SSEClient(f"{self.link_api}.json?auth={self.id_token}")
                if self.cont_reconexao >0:
                    self.info_geral_build.texto_info_geral.texture_update()
                    self.status_conexao_internet = True

                    
                    Clock.schedule_once(lambda dt:self.gerenciamento_conexao(erro=None), 0)
                    
                    self.cont_reconexao = 0
                for evento in sseclient:
                    if evento.data and evento.data != "null":
                        try:
                            data = json.loads(evento.data)
                            if "data" in data:
                                caminho = data.get("path", "/")
                                if caminho == "/":
                                    self.db_api = data["data"]
                                    Clock.schedule_once(lambda dt: self.strem_db(db=self.db_api), 0)
                                    
                                else:
                                    resposa = requests.get(f"{self.link_api}.json?auth={self.id_token}")
                                    if resposa.status_code !=200:
                                        Clock.schedule_once(self.gerenciamento_info_geral(msg=f"(!) Erro na solicitação: {resposa.status_code}"), 0)
                                    else:
                                       self.db_api = resposa.json()
                                       Clock.schedule_once(lambda dt: self.strem_db(db=self.db_api), 0)
                        except Exception as erro:
                            # Pode adicionar log ou tratamento aqui
                            pass
                    else:
                        # Aqui poderia abrir um popup de erro apenas uma vez
                        pass
            except requests.exceptions.ConnectionError as erro:
                self.reconexao = True
                self.cont_reconexao +=1
                msg_erro = erro
                self.status_conexao_internet = None
                if self.status_conexao_internet is None and self.cont_reconexao ==1:
                    
                    Clock.schedule_once(lambda dt: self.gerenciamento_conexao(erro=msg_erro), 0)


                
                time.sleep(self.cont_reconexao)
                
            except Exception as erro:
                    pass
 
    def gerenciamento_conexao(self, erro):
        if self.status_conexao_internet == None:

            setattr(self.info_geral_build.texto_info_geral, "text", f"[b][color=#ff0000](!) Sem acesso a internet![b]\n[i][color=#ffff00]Erro: {str(erro)}")
            
            self.info_geral_build.texto_info_geral.texture_update()
            self.info_geral_build.atua_tam_fonte()
    
            self.info_geral_build.open()
            self.info_geral_build.texto_info_geral.opacity = 0
            AnimacaoTextos(instance=self.info_geral_build.texto_info_geral, duracao=2)
            
        else:
            setattr(self.info_geral_build.texto_info_geral, "text", "[color=00ff00](!) Conexão restabelecida!")
            self.info_geral_build.texto_info_geral.texture_update()
            self.info_geral_build.atua_tam_fonte()
            self.info_geral_build.open()
            
            self.info_geral_build.texto_info_geral.opacity = 0
            AnimacaoTextos(instance=self.info_geral_build.texto_info_geral, duracao=1)
            
            Clock.schedule_once(lambda dt: self.info_geral_build.dismiss(), 2.5)
            
            
    def strem_db(self, db=None):
        try:
            self.db_api = db
            if self.usuario_verificado is True:
                
                #Clock.schedule_once(lambda dt, *args:self.tela_inicial.diario_oficial(db_api=self.db_api),0)
                Clock.schedule_once(lambda dt: self.tela_compras.organizar_mercadorias(), 0)
                
                Clock.schedule_once(lambda dt: self.tela_inicial.organizador_oferta(), 0)
                
                Clock.schedule_once(lambda dt: self.tela_os.organizador_widgets_items(), 0)
                
                
            else:
                if os.path.exists(os.path.join(app_storage_path(), "login_usuario.json")):
                    os.remove(os.path.join(app_storage_path(), "login_usuario.json"))
                    
                    
            
        except Exception as erro:
            msg_erro = erro
            InfoGeral(arg=f"(!) Erro crítico em build!\n def stream_db\n [color=#ffff00]{msg_erro}\n{traceback.format_exc()}").open()

if __name__ == "__main__":
    MeuApp().run()
    