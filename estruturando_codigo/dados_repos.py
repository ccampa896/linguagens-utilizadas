import requests
import pandas as pd

class DadosRepositorios:

    def __init__(self, owner):
        self.owner = owner
        self.api_base_url = 'https://api.github.com'
        self.access_token = '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'
        self.headers = {'Authorization': 'Bearer ' + self.access_token,
                        'X-GitHub-Api-Version': '2022-11-28'}

    def lista_repositorios(self):
        repos_list = []

        qtd_repos = requests.get(f'{self.api_base_url}/users/{self.owner}').json()['public_repos']
        qtd_pages = (qtd_repos // 30) + 1

        for page_num in range(1, qtd_pages + 1):
            try:
                url = f'{self.api_base_url}/users/{self.owner}/repos?page={page_num}'
                response = requests.get(url, headers=self.headers)
                repos_list.append(response.json())
            except:
                repos_list.append(None)

        return repos_list

    def nomes_repos(self, repos_list):
        repos_name = []
        for page in repos_list:
            for repo in page:
                try:
                    repos_name.append(repo['name'])
                except:
                    pass

        return repos_name

    def nomes_linguagens(self, repos_list):
        repos_lang = []
        for page in repos_list:
            for repo in page:
                try:
                    repos_lang.append(repo['language'])
                except:
                    pass

        return repos_lang

    def cria_df_linguagem(self):

        repositorios = self.lista_repositorios()
        nomes = self.nomes_repos(repositorios)
        linguagens = self.nomes_linguagens(repositorios)

        df = pd.DataFrame({'nome': nomes, 'linguagem': linguagens})

        return df