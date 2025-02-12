class HistoricoUsuario:
    def __init__(self, id_usuario,
                 id_questao, acerto, tempo_resposta, erro, id_historico):
        self._id_historico = id_historico
        self._id_usuario = id_usuario
        self._id_questao = id_questao
        self._acerto = acerto
        self._tempo_resposta = tempo_resposta
        self._erro = erro

    # Getters
    @property
    def id_historico(self):
        return self._id_historico

    @property
    def id_usuario(self):
        return self._id_usuario

    @property
    def id_questao(self):
        return self._id_questao

    @property
    def acerto(self):
        return self._acerto

    @property
    def tempo_resposta(self):
        return self._tempo_resposta

    @property
    def erro(self):
        return self._erro

    # Setters
    @id_usuario.setter
    def id_usuario(self, id_usuario):
        self._id_usuario = id_usuario

    @id_questao.setter
    def id_questao(self, id_questao):
        self._id_questao = id_questao

    @acerto.setter
    def acerto(self, acerto):
        self._acerto = acerto

    @tempo_resposta.setter
    def tempo_resposta(self, tempo_resposta):
        self._tempo_resposta = tempo_resposta

    @erro.setter
    def erro(self, erro):
        self._erro = erro
