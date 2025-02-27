from playwright.sync_api import sync_playwright
import json
import html
import csv

class ProfessorOnlineScraper:
    def __init__(self, cpf, senha):
        self.cpf = cpf
        self.senha = senha
        self.navegador = None
        self.pagina = None
    
    def iniciar_navegador(self):
        """Inicia o navegador e a página."""
        self.navegador = sync_playwright().start().chromium.launch(headless=False)  # Abrir o navegador
        self.pagina = self.navegador.new_page()  # Nova página

    def fazer_login(self):
        """Realiza o login no site."""
        self.pagina.goto('https://professoronline.sed.sc.gov.br/cadloginprofcaptchacopy1.aspx')
        self.pagina.fill('xpath=//*[@id="vCPF"]', self.cpf)
        self.pagina.fill('xpath=//*[@id="vSENHA"]', self.senha)
        self.pagina.locator('xpath=//*[@id="TABLE1"]/tbody/tr[9]/td/span/span/span/span/input').click()

    def capturar_dados(self, id):
        """Captura os dados da tabela e retorna como uma lista de listas."""
        salas = self.pagina.locator(id)
        valor_json_codificado = salas.get_attribute("value")
        valor_json_decodificado = html.unescape(valor_json_codificado)
        dados = json.loads(valor_json_decodificado)
        return dados

    def montar_csv_turmas(self, dados, arquivo_csv):
        """Cria um arquivo CSV com as informações coletadas."""
        with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(["Escola", "Série", "Turma"])
            for linha in dados:
                nome_escola = linha[4]
                serie = linha[10]
                turma = linha[11]
                escritor.writerow([nome_escola, serie, turma])
    
    
    def montar_csv_notas(self, dados, arquivo_csv):
        """Cria um arquivo CSV com as informações coletadas."""
        with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(["Aluno", "Atividade1", "Atividade2"])
            for linha in dados:
                nome = linha[1]
                atv1 = linha[2]
                atv2 = linha[3]
                escritor.writerow([nome, atv1, atv2])

    def fechar_navegador(self):
        """Fecha o navegador."""
        if self.navegador:
            self.navegador.close()

    """   def selecionar_turma(self):
        self.pagina.locator(f"//*[@id="span_vDTAUENOM_000{i}"]/a")
    """

def main():
    cpf = ''
    senha = ''

    # Criar a instância do scraper
    scraper = ProfessorOnlineScraper(cpf, senha)

    # Iniciar o navegador e fazer login
    scraper.iniciar_navegador()
    scraper.fazer_login()

    # Capturar os dados - Turmas
    dados = scraper.capturar_dados('xpath=//*[@id="TABLE2"]/tbody/tr/td/input')

    # Criar o arquivo CSV - Turmas
    scraper.montar_csv_turmas(dados, "turmas.csv")

    # Selecionar turma 1
    scraper.pagina.locator('xpath=//*[@id="span_vDTAUENOM_0001"]/a').click()
    # Ir para notas
    scraper.pagina.locator('//*[@id="scabreadcrumb"]/li[2]/a').click()

    # Capturar os dados - Notas
    dados2 = scraper.capturar_dados('xpath=//*[@id="Grid1ContainerDiv"]')

    # Criar o arquivo CSV - Notas
    scraper.montar_csv_turmas(dados2, "notas.csv")
    
    # Fechar o navegador
    scraper.fechar_navegador()

if __name__ == "__main__":
    main()


"""
-=-=-=-=-=-=  OBSERVAÇÕES  -=-=-=-=-=-=
1- Ao invés de usar with sync_playwright() as p diretamente, a função start() é chamada para garantir que o Playwright é 
iniciado corretamente. Isso pode ser necessário para garantir que o fluxo assíncrono do Playwright não seja interrompido prematuramente.
"""