FROM node:18

WORKDIR /var/www/html

COPY package.json package-lock.json ./

RUN npm install
ENV FLAG=squ1rrel{fakeflag}
ENV SECRET_KEY=secret

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
