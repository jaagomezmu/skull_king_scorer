class RegistroRonda:
    def __init__(self, mano, cartas_repartidas, envite, tipo_envite, resultado, bonificaciones=0):
        self.mano = mano
        self.cartas_repartidas = cartas_repartidas
        self.envite = envite
        self.tipo_envite = tipo_envite
        self.resultado = resultado
        self.bonificaciones = bonificaciones
        self.puntos_mano = self.calcular_puntos()
        self.total_actual = 0 

    def calcular_puntos(self):
        if self.envite == self.resultado:
            if self.envite == 0:
                return (10 * self.mano) + self.bonificaciones
            else:
                return (20 * self.envite) + self.bonificaciones
        else:
            if self.envite == 0:
                return (-10 * self.mano) + self.bonificaciones
            else:
                return (-10 * abs(self.envite - self.resultado)) + self.bonificaciones


class Player:
    def __init__(self, name):
        self.name = name
        self.total = 0
        self.historial = []

    def registrar_ronda(self, registro):
        registro.total_actual = self.total + registro.puntos_mano
        self.total += registro.puntos_mano
        self.historial.append(registro)


class Game:
    def __init__(self, player_names, total_rondas):
        self.players = [Player(name) for name in player_names]
        self.total_rondas = total_rondas
        self.ronda_actual = 0

    def play_round(self):
        self.ronda_actual += 1
        print(f"\n--- Ronda {self.ronda_actual} ---")

        cartas = self.ronda_actual

        apuestas = {}
        resultados = {}
        bonificaciones = {}

        # Apuestas
        print("\nApuestas:")
        for player in self.players:
            while True:
                try:
                    apuesta = int(input(f"{player.name} - ¿Cuántas bazas apuestas?: "))
                    apuestas[player.name] = apuesta
                    break
                except ValueError:
                    print("Ingresa un número válido.")

        # Resultados
        print("\nResultados reales:")
        for player in self.players:
            while True:
                try:
                    resultado = int(input(f"{player.name} - ¿Cuántas ganaste?: "))
                    resultados[player.name] = resultado
                    break
                except ValueError:
                    print("Ingresa un número válido.")

        # Bonificaciones
        print("\nBonificaciones (si aplica):")
        for player in self.players:
            try:
                bonus = int(input(f"{player.name} - Bonificación (enter = 0): ") or 0)
            except ValueError:
                bonus = 0
            bonificaciones[player.name] = bonus

        # Registrar ronda
        for player in self.players:
            envite = apuestas[player.name]
            resultado = resultados[player.name]
            bonus = bonificaciones[player.name]
            tipo = "Cero" if envite == 0 else "Normal"

            registro = RegistroRonda(
                mano=self.ronda_actual,
                cartas_repartidas=cartas,
                envite=envite,
                tipo_envite=tipo,
                resultado=resultado,
                bonificaciones=bonus
            )

            player.registrar_ronda(registro)

    def show_scores(self):
        print("\nPuntuaciones acumuladas:")
        for player in self.players:
            print(f"{player.name}: {player.total} puntos")

    def resumen_final(self):
        print("\nRESUMEN FINAL:")
        for player in self.players:
            print(f"\n{player.name}: {player.total} puntos totales")
            for r in player.historial:
                print(f"  Ronda {r.mano}: envite={r.envite}, ganó={r.resultado}, tipo={r.tipo_envite}, "
                      f"bonus={r.bonificaciones}, pts ronda={r.puntos_mano}, total={r.total_actual}")


if __name__ == "__main__":
    nombres = input("***** Nombres de jugadores separados por coma: ").split(",")
    nombres = [n.strip() for n in nombres if n.strip()]
    while True:
        try:
            rondas = int(input("¿Cuántas rondas quieres jugar?: "))
            break
        except ValueError:
            print("Ingresa un número entero válido.")

    game = Game(nombres, rondas)

    for _ in range(rondas):
        game.play_round()
        game.show_scores()

    game.resumen_final()
