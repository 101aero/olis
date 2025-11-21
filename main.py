# CAFEBAKS v0.2
# Simulación básica de una cafetería tipo franquicia en Madrid

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


# ---------------------------------------------------------
# MODELO SENCILLO DEL JUEGO (datos de la cafetería)
# ---------------------------------------------------------
class EstadoJuego:
    def __init__(self):
        # Nombre de la cafetería (se puede cambiar más adelante)
        self.nombre_cafeteria = "CafeBAKS Madrid"
        # Ciudad y zona
        self.ciudad = "Madrid - Gran Vía"
        # Día de la simulación (empieza en el día 1)
        self.dia = 1
        # Dinero en caja (saldo inicial)
        self.saldo = 500.0  # euros


# ---------------------------------------------------------
# PANTALLA 1: MENÚ PRINCIPAL
# ---------------------------------------------------------
class MenuPrincipal(Screen):
    def __init__(self, estado_juego: EstadoJuego, **kwargs):
        super().__init__(**kwargs)

        self.estado = estado_juego  # referencia al estado común del juego

        # Layout vertical
        layout = BoxLayout(orientation="vertical",
                           padding=20,
                           spacing=20)

        # Etiqueta principal donde se muestra la información del negocio
        self.lbl_info = Label(
            text=self._generar_texto_info(),
            halign="center"
        )

        # Botón para simular un día de ventas
        btn_dia = Button(text="Abrir un día de ventas")
        btn_dia.bind(on_press=self.simular_dia_ventas)

        # Botón para ir a la pantalla de "tienda" (más opciones en el futuro)
        btn_tienda = Button(text="Ver detalles de la tienda")
        btn_tienda.bind(on_press=self.ir_a_tienda)

        # Añadir widgets al layout
        layout.add_widget(self.lbl_info)
        layout.add_widget(btn_dia)
        layout.add_widget(btn_tienda)

        self.add_widget(layout)

    def _generar_texto_info(self) -> str:
        """
        Genera el texto que resume el estado actual de la cafetería.
        """
        return (
            f"{self.estado.nombre_cafeteria}\n"
            f"{self.estado.ciudad}\n\n"
            f"Día: {self.estado.dia}\n"
            f"Saldo en caja: {self.estado.saldo:.2f} €"
        )

    def simular_dia_ventas(self, instance):
        """
        Simula un día de ventas muy simple:
        - Aumenta el saldo en una cantidad fija (beneficio del día).
        - Avanza el contador de días.
        Más adelante aquí se añaden clientes, gastos, etc.
        """
        beneficio_dia = 120.0  # por ahora, cifra fija
        self.estado.saldo += beneficio_dia
        self.estado.dia += 1

        # Actualiza el texto de la etiqueta con los nuevos datos
        self.lbl_info.text = self._generar_texto_info()

    def ir_a_tienda(self, instance):
        """
        Cambia a la pantalla 'tienda'.
        """
        self.manager.current = "tienda"


# ---------------------------------------------------------
# PANTALLA 2: TIENDA
# (en el futuro: productos, precios, stock, personal, etc.)
# ---------------------------------------------------------
class PantallaTienda(Screen):
    def __init__(self, estado_juego: EstadoJuego, **kwargs):
        super().__init__(**kwargs)

        self.estado = estado_juego

        layout = BoxLayout(orientation="vertical",
                           padding=20,
                           spacing=20)

        # Etiqueta que muestra datos resumidos
        self.lbl_resumen = Label(
            text=self._generar_resumen(),
            halign="center"
        )

        # Botón para volver al menú principal
        btn_volver = Button(text="Volver al menú principal")
        btn_volver.bind(on_press=self.volver_menu)

        layout.add_widget(self.lbl_resumen)
        layout.add_widget(btn_volver)

        self.add_widget(layout)

    def _generar_resumen(self) -> str:
        """
        Muestra un pequeño resumen del estado del juego.
        Más adelante puede incluir lista de productos, empleados, etc.
        """
        return (
            f"Resumen de la tienda\n\n"
            f"Nombre: {self.estado.nombre_cafeteria}\n"
            f"Ubicación: {self.estado.ciudad}\n"
            f"Día actual: {self.estado.dia}\n"
            f"Saldo: {self.estado.saldo:.2f} €"
        )

    def on_pre_enter(self, *args):
        """
        Antes de entrar en la pantalla, se actualiza el resumen
        por si han cambiado datos (día, saldo, etc.).
        """
        self.lbl_resumen.text = self._generar_resumen()

    def volver_menu(self, instance):
        self.manager.current = "menu"


# ---------------------------------------------------------
# GESTOR DE PANTALLAS
# ---------------------------------------------------------
class GestorPantallas(ScreenManager):
    pass


# ---------------------------------------------------------
# APLICACIÓN PRINCIPAL
# ---------------------------------------------------------
class CafeBaksApp(App):

    def build(self):
        # Se crea el estado común del juego (modelo de la cafetería)
        estado = EstadoJuego()

        # Gestor de pantallas
        sm = GestorPantallas()

        # Se pasan las referencias de estado a cada pantalla
        sm.add_widget(MenuPrincipal(estado, name="menu"))
        sm.add_widget(PantallaTienda(estado, name="tienda"))

        return sm


# ---------------------------------------------------------
# EJECUCIÓN
# ---------------------------------------------------------
if __name__ == "__main__":
    CafeBaksApp().run()