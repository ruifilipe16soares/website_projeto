# Use uma imagem base oficial do Nginx
FROM nginx:alpine

# Copie os arquivos da aplicação para o diretório padrão do Nginx
COPY . /usr/share/nginx/html

# Exponha a porta 80
EXPOSE 80

# O Nginx será executado automaticamente quando o contêiner for iniciado
