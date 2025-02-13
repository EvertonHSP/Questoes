from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QMessageBox,
    QStackedWidget,
    QFrame,
    QGridLayout  # Adicione esta linha
)
from PyQt5.QtGui import QPixmap, QFont, QPalette, QBrush
from PyQt5.QtCore import Qt
from PIL import Image
from io import BytesIO
from PyQt5.QtWidgets import QFrame


class InterfaceApp(QMainWindow):

    def __init__(self, intermediary_manager):
        super().__init__()
        self.intermediary_manager = intermediary_manager
        self.current_question = None
        self.questoes_sugeridas = []
        self.modo_sugestao = False
        self.id_usuario = None

        # Configurações iniciais da janela
        self.setWindowTitle("Quiz App")
        self.setGeometry(100, 100, 800, 600)

        self.background_image_path = "bg.jpg"  # Substitua pelo caminho da imagem
        self.set_background_image(self.background_image_path)

        # Cria o QStackedWidget para gerenciar as telas
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Tela de login
        self.login_screen = self.create_login_screen()
        self.stacked_widget.addWidget(self.login_screen)

        # Tela intermediária
        self.intermediate_screen = self.create_intermediate_screen()
        self.stacked_widget.addWidget(self.intermediate_screen)

        # Tela principal do quiz
        self.quiz_screen = self.create_quiz_screen()
        self.stacked_widget.addWidget(self.quiz_screen)

        # Tela de cadastro
        self.cadastro_screen = self.create_cadastro_screen()
        self.stacked_widget.addWidget(self.cadastro_screen)

        # Tela de desempenho
        self.desempenho_screen = self.create_desempenho_screen()
        self.stacked_widget.addWidget(self.desempenho_screen)

        # Mostra a tela de login inicialmente
        self.stacked_widget.setCurrentIndex(0)

    def set_background_image(self, image_path):
        """Define uma imagem como plano de fundo da janela."""
        pixmap = QPixmap(image_path)  # Carrega a imagem

        # Redimensiona a imagem para cobrir toda a janela
        scaled_pixmap = pixmap.scaled(
            self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        # Cria um QBrush a partir do QPixmap
        brush = QBrush(scaled_pixmap)

        palette = self.palette()
        # Define o QBrush como plano de fundo
        palette.setBrush(QPalette.Background, brush)
        self.setPalette(palette)

    def resizeEvent(self, event):
        """Redimensiona a imagem de fundo quando a janela é redimensionada."""
        super().resizeEvent(event)
        self.set_background_image(self.background_image_path)

    def create_login_screen(self):
        """Cria a tela de login."""
        screen = QWidget()
        # Usa QGridLayout para centralização dinâmica
        screen_layout = QGridLayout(screen)
        screen_layout.setAlignment(Qt.AlignCenter)  # Centraliza o conteúdo

        # Cria um QFrame para o retângulo preto semi-transparente
        frame = QFrame()
        frame.setStyleSheet("""
            background-color: rgba(0, 0, 0, 50);  /* Preto com 60% de opacidade */
            border-radius: 15px;
        """)
        frame.setFixedSize(400, 300)  # Tamanho do retângulo
        frame_layout = QVBoxLayout(frame)
        frame_layout.setAlignment(Qt.AlignCenter)

        # Título
        title = QLabel("Autenticação")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("""
            background-color: rgba(0, 0, 0, 50);  /* Preto com 40% de opacidade */
            color: white;
            border-radius: 10px;  /* Bordas arredondadas */
            padding: 10px;  /* Espaçamento interno */
        """)
        title.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(title)

        # Campo de email
        self.email_entry = QLineEdit()
        self.email_entry.setPlaceholderText("Email")
        self.email_entry.setStyleSheet("""
            background-color: rgba(255, 255, 255, 80);  
            color: white;  
            border: 1px solid white;  
            border-radius: 5px; 
            padding: 10px; 
            font-weight: bold;  
        """)
        frame_layout.addWidget(self.email_entry)

        # Campo de senha
        self.senha_entry = QLineEdit()
        self.senha_entry.setPlaceholderText("Senha")
        self.senha_entry.setEchoMode(QLineEdit.Password)
        self.senha_entry.setStyleSheet("""
            background-color: rgba(255, 255, 255, 80);  
            color: white;  
            border: 1px solid white;  
            border-radius: 5px; 
            padding: 10px; 
            font-weight: bold;  
        """)
        frame_layout.addWidget(self.senha_entry)

        # Botão de entrar
        entrar_button = QPushButton("Entrar")
        entrar_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 60);  
                color: white;   
                border-radius: 5px; 
                padding: 10px; 
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 120);  /* Opacidade aumentada ao passar o mouse */
            }                        
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 240);  
            }
        """)
        entrar_button.clicked.connect(self.verificar_autenticacao)
        frame_layout.addWidget(entrar_button)

        # Botão de criar cadastro
        cadastro_button = QPushButton("Criar Cadastro")
        cadastro_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 60);  
                color: white; 
                border-radius: 5px; 
                padding: 10px; 
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 120);  /* Opacidade aumentada ao passar o mouse */
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 240);  
            }
        """)
        cadastro_button.clicked.connect(self.show_cadastro_screen)
        frame_layout.addWidget(cadastro_button)

        # Adiciona o frame ao layout da tela
        screen_layout.addWidget(frame, 0, 0, alignment=Qt.AlignCenter)

        return screen

    def create_intermediate_screen(self):
        """Cria a tela intermediária após o login."""
        screen = QWidget()
        layout = QVBoxLayout()

        # Título
        title = QLabel("Bem-vindo ao Quiz!")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("""
            color: white;
            padding: 10px;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Botão "Começar Quiz"
        comecar_button = QPushButton("Começar Quiz")
        comecar_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 60);  
                color: white; 
                border-radius: 5px; 
                padding: 10px; 
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 120);  /* Opacidade aumentada ao passar o mouse */
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 240);  
            }
        """)
        comecar_button.clicked.connect(
            self.show_quiz_screen)  # Redireciona para a tela do quiz
        layout.addWidget(comecar_button)

        screen.setLayout(layout)
        return screen

    def create_cadastro_screen(self):
        """Cria a tela de cadastro."""
        screen = QWidget()
        screen_layout = QVBoxLayout(screen)

        # Cria um QFrame para o retângulo preto semi-transparente
        frame = QFrame()
        frame.setStyleSheet("""
            background-color: rgba(0, 0, 0, 50);  /* Preto com 60% de opacidade */
            border-radius: 15px;
        """)
        frame.setFixedSize(400, 300)  # Tamanho do retângulo
        frame_layout = QVBoxLayout(frame)
        frame_layout.setAlignment(Qt.AlignCenter)

        # Título
        title = QLabel("Criar Cadastro")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("""
            background-color: rgba(0, 0, 0, 50);  /* Preto com 40% de opacidade */
            color: white;
            border-radius: 10px;  /* Bordas arredondadas */
            padding: 10px;  /* Espaçamento interno */
        """)
        title.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(title)

        # Campo de nome
        self.nome_entry = QLineEdit()
        self.nome_entry.setPlaceholderText("Nome")
        self.nome_entry.setStyleSheet("""
            background-color: rgba(255, 255, 255, 80);  
            color: white;  
            border: 1px solid white;  
            border-radius: 5px; 
            padding: 10px; 
            font-weight: bold;
        """)
        frame_layout.addWidget(self.nome_entry)

        # Campo de email
        self.email_cadastro_entry = QLineEdit()
        self.email_cadastro_entry.setPlaceholderText("Email")
        self.email_cadastro_entry.setStyleSheet("""
            background-color: rgba(255, 255, 255, 80);  
            color: white;  
            border: 1px solid white;  
            border-radius: 5px; 
            padding: 10px; 
            font-weight: bold;
        """)
        frame_layout.addWidget(self.email_cadastro_entry)

        # Campo de senha
        self.senha_cadastro_entry = QLineEdit()
        self.senha_cadastro_entry.setPlaceholderText("Senha")
        self.senha_cadastro_entry.setEchoMode(QLineEdit.Password)
        self.senha_cadastro_entry.setStyleSheet("""
            background-color: rgba(255, 255, 255, 80);  
            color: white;  
            border: 1px solid white;  
            border-radius: 5px; 
            padding: 10px; 
            font-weight: bold;
        """)
        frame_layout.addWidget(self.senha_cadastro_entry)

        # Botão de confirmar cadastro
        confirmar_button = QPushButton("Confirmar")
        confirmar_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 60);  
                color: white; 
                border-radius: 5px; 
                padding: 10px; 
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 120);  /* Opacidade aumentada ao passar o mouse */
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 240);  
            }
        """)
        confirmar_button.clicked.connect(self.confirmar_cadastro)
        frame_layout.addWidget(confirmar_button)

        # Botão de voltar
        voltar_button = QPushButton("Voltar")
        voltar_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 60);  
                color: white; 
                border-radius: 5px; 
                padding: 10px; 
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 120);  /* Opacidade aumentada ao passar o mouse */
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 240);  
            }
        """)
        voltar_button.clicked.connect(self.show_login_screen)
        frame_layout.addWidget(voltar_button)

        # Adiciona o frame ao layout da tela
        screen_layout.addWidget(frame, alignment=Qt.AlignCenter)

        return screen

    def create_quiz_screen(self):
        """Cria a tela principal do quiz."""
        screen = QWidget()
        layout = QVBoxLayout()

        # Label para exibir a imagem da questão
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        # Frame para os botões de alternativas
        buttons_layout = QHBoxLayout()
        self.buttons = []
        for option in ["A", "B", "C", "D", "E"]:
            button = QPushButton(option)
            button.setFixedSize(100, 50)
            button.clicked.connect(
                lambda _, o=option: self.check_answer(o))
            buttons_layout.addWidget(button)
            self.buttons.append(button)
        layout.addLayout(buttons_layout)

        # Botão para ver desempenho
        self.desempenho_button = QPushButton("Ver Desempenho")
        self.desempenho_button.clicked.connect(self.mostrar_desempenho)
        layout.addWidget(self.desempenho_button)

        screen.setLayout(layout)
        return screen

    def create_desempenho_screen(self):
        """Cria a tela de desempenho."""
        screen = QWidget()
        layout = QVBoxLayout()

        # Label para exibir o desempenho
        self.desempenho_label = QLabel()
        self.desempenho_label.setFont(QFont("Arial", 14))
        self.desempenho_label.setAlignment(Qt.AlignCenter)
        self.desempenho_label.setWordWrap(True)
        layout.addWidget(self.desempenho_label)

        # Botão para fechar
        fechar_button = QPushButton("Fechar")
        fechar_button.clicked.connect(self.show_quiz_screen)
        layout.addWidget(fechar_button)

        screen.setLayout(layout)
        return screen

    def show_login_screen(self):
        """Mostra a tela de login."""
        self.stacked_widget.setCurrentIndex(0)

    def show_intermediate_screen(self):
        """Mostra a tela intermediária após o login."""
        self.stacked_widget.setCurrentIndex(1)  # Índice da tela intermediária

    def show_cadastro_screen(self):
        """Mostra a tela de cadastro."""
        self.stacked_widget.setCurrentIndex(2)

    def show_quiz_screen(self):
        """Mostra a tela do quiz."""
        self.stacked_widget.setCurrentIndex(2)  # Índice da tela do quiz
        self.iniciar_quiz()

    def show_desempenho_screen(self):
        """Mostra a tela de desempenho."""
        self.stacked_widget.setCurrentIndex(3)

    def verificar_autenticacao(self):
        """Verifica se o usuário está autenticado."""
        email = self.email_entry.text()
        senha = self.senha_entry.text()
        self.id_usuario = self.intermediary_manager.autenticar_usuario(
            email, senha)

        if self.id_usuario:
            self.show_intermediate_screen()  # Redireciona para a tela intermediária
        else:
            QMessageBox.critical(self, "Erro", "Email ou senha incorretos.")

    def confirmar_cadastro(self):
        """Confirma o cadastro do usuário."""
        nome = self.nome_entry.text()
        email = self.email_cadastro_entry.text()
        senha = self.senha_cadastro_entry.text()

        if not nome or not email or not senha:
            QMessageBox.critical(
                self, "Erro", "Todos os campos são obrigatórios.")
            return

        try:
            self.intermediary_manager.adicionar_usuario(nome, email, senha)
            QMessageBox.information(
                self, "Sucesso", "Cadastro realizado com sucesso!")
            self.show_login_screen()
        except Exception as e:
            QMessageBox.critical(
                self, "Erro", f"Erro ao criar cadastro: {str(e)}")

    def iniciar_quiz(self):
        """Inicia o quiz após o login bem-sucedido."""
        self.next_question()

    def next_question(self):
        """Carrega a próxima questão."""
        if self.modo_sugestao:
            id_sugerida, questao_sugerida = self.intermediary_manager.sugerir_questao(
                self.current_question.area,
                self.current_question.id_questao,
                self.questoes_sugeridas,
            )
            if questao_sugerida:
                self.current_question = questao_sugerida
            else:
                QMessageBox.information(
                    self, "Info", "Nenhuma questão sugerida disponível.")
                self.modo_sugestao = False
                self.current_question = None
        else:
            self.current_question = self.intermediary_manager.enviar_questao_aleatoria()

        if self.current_question:
            self.display_question(self.current_question)
        else:
            QMessageBox.information(
                self, "Fim", "Não há mais questões disponíveis.")

    def display_question(self, question):
        """Exibe a questão na interface."""
        try:
            image = Image.open(question.imagem)
            image = image.resize((600, 400), Image.Resampling.LANCZOS)
            image_bytes = BytesIO()
            image.save(image_bytes, format="PNG")
            pixmap = QPixmap()
            pixmap.loadFromData(image_bytes.getvalue())
            self.image_label.setPixmap(pixmap)
        except Exception as e:
            QMessageBox.critical(
                self, "Erro", f"Não foi possível carregar a imagem: {e}")

    def check_answer(self, selected_option):
        """Verifica se a resposta está correta."""
        if self.current_question:
            resposta_correta = self.current_question.resposta_correta.strip().lower()
            selected_option_normalized = selected_option.strip().lower()

            acerto_erro = 1 if selected_option_normalized == resposta_correta else 0

            self.intermediary_manager.registrar_resposta(
                self.id_usuario, self.current_question.id_questao, acerto_erro
            )

            if acerto_erro:
                QMessageBox.information(self, "Resposta", "Correto!")
                self.modo_sugestao = False
                self.questoes_sugeridas.clear()
            else:
                QMessageBox.information(
                    self, "Resposta", "Errado! Buscando uma questão similar...")
                self.modo_sugestao = True

            self.next_question()

    def mostrar_desempenho(self):
        """Mostra a tela de desempenho."""
        if self.id_usuario:
            desempenho = self.intermediary_manager.calcular_desempenho(
                self.id_usuario)
        else:
            desempenho = "Usuário não autenticado."

        self.desempenho_label.setText(desempenho)
        self.show_desempenho_screen()
