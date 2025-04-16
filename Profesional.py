class Profesional:
    def __init__(self, id, nombre, email, especialidad):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.especialidad = especialidad
        self.servicios = []

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)

    def mostrar_datos(self):
        return f"Profesional: {self.nombre} ({self.especialidad}) - Email: {self.email}"

    def __repr__(self):
        return f"<Profesional id={self.id} nombre={self.nombre}>"