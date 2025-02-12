from Models.Prova import Prova


class ProvaDAO:
    def __init__(self, connection):
        self.connection = connection

    def get_provas(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM prova")
        return [Prova(*data) for data in cursor.fetchall()]

    def add_prova(self, banca, ano, infor):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO prova (banca, ano, infor) VALUES (?, ?, ?)",
            (banca, ano, infor))
        self.connection.commit()
