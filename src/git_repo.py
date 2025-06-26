
# Instale o git-filter-repo se ainda não tiver
brew install git-filter-repo  # macOS
sudo apt install git-filter-repo  # Ubuntu/Debian

# Remova o arquivo do histórico
git filter-repo --path dados/fundos_abril_maio_2024.csv --invert-paths
