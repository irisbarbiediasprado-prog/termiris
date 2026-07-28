import subprocess

class SystemQueryProvider:
    @staticmethod
    def tree(dir_path: str) -> str:
        try:
            res = subprocess.run(
                ["fd", "--max-depth", "3", "--exclude", ".git", "--exclude", "cache", ".", dir_path],
                capture_output=True, text=True, check=True
            )
            return res.stdout if res.stdout.strip() else f"Diretório vazio ou inacessível: {dir_path}"
        except Exception as e:
            return f"Erro ao mapear diretório com fd: {e}"

    @staticmethod
    def search(query: str) -> str:
        try:
            res = subprocess.run(
                ["rg", "--no-heading", "--line-number", "--color", "never", "-g", "!.git/*", "-g", "!cache/*", query, "."],
                capture_output=True, text=True
            )
            lines = res.stdout.splitlines()[:30]
            return "\n".join(lines) if lines else f"Nenhum resultado para: {query}"
        except Exception as e:
            return f"Erro ao executar busca com rg: {e}"

