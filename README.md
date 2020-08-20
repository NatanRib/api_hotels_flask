#Rest api de hoteis feita com flask, banco de dados sq-lite e autenticação JWT

Aplicação robusta, feita para consolidar meus conhecimentos com essa tecnologia. É uma aplicação semelhante ao Trivago, contem a função de cadastar sites e hoteis atrelados a esses site, onde cada site tem n hoteis em uma relação de composição 'one to many'. Para que seja autorizado o cadastro de hoteis e sites o cliente precisar criar uma conta e loga-la. Foi utilizado Flask, Flask restful, flask jwt extended e sq-lite

##Instalação:

    * necessita de python3.8
    * instalar os modulos: pip3 install -r requirements.txt
    * para rodar: python3 app.py
    * roda no localhost porta 5000 

##Respostas:

    * todas as respostas são em formato Json, todos os erros tem sua resposta em Json com um atributo 'mensage', explicando oque ocasionou o erro.


##Cadastro de usuario, login, logout:

###Cadastro /singup:

    * O cadastro recebe os os seguintes parametros obrigatorio no corpo da requisição:
        * username => Nome de usuario
        * password => Senha

####Exemplo de requisição:

    POST localhost:5000/singup

    body {
            "username": "natanrib",
            "password": "123456"
        }

###Login /login:

    * Muitos dos recursos dessa API precisam que o cliente esteja autenticado, para isso realizamos o login. Esse recurso nos da uma resposta com o token JWT de autenticação da sessão.

####Exemplo de requisição:

    POST localhost:5000/login

    body {
            "username": "natanrib",
            "password": "123456"
        }

###Resposta:

    * A resposta de um login é o token de acesso, precisamos passar esse token de acesso no atributo Authorization do header em todo recurso que exige autenticação.

    Response {
                "access_token": "tokendeacesso" 
            }

###Logout /logout:

    * Para deslogar um usuario usaremos esse recurso, precisamos acessar a rota e passar no Header nosso token, ao faze-lo o token de acesso é colocado em um blacklist para a aplicação saber que esse token esta deslogado.

####Exemplo de requisição:

    POST localhost:5000/logout

    Header: Authorization = Bearer "token de acesso" - precisamos antes do token ter a palavra "Bearer" para indentificar que estamos mandando um token e não um usuario e senha.

###Deletar um usuario /users/username:

    * Usamos o seguinte recurso para deletar um usuario, precisamos estar autenticados e passa o username dele na rota

####Exemplo de requisição:

    DELETE localhost:5000/users/<username> - passamos o username do usuario a ser deletado

    Header: Authorization = Bearer "token de acesso" - precisamos antes do token ter a palavra "Bearer" para indentificar que estamos mandando um token e não um usuario e senha. 

###Recuperar um usuario pelo username(TESTES) /users/username:

    * Essa funcão é apenas para testes, não faz sentido tela em um sistema real, com ela recuperamos os dados de um usuario passando seu login na rota

####Exemplo de requisição:

    GET localhost:5000/users/<username>

    Response: {
                "username": "username",
                "password": "password"
            }

###Recuperar todos os usuarios(TESTES) /users:

    * Essa função é apenas pra testes, não faz sentido tela em um sistema real, com ela recuperamos todos os usuarios

####Exemplo de requisição:

    GET localhost:5000/users

    Response: {
                "users": [
                    {
                        "username": "username",
                        "password": "password"
                    }
                ]
            }


##Consultar sites, cadastrar e deletar:

###Consultar /sites: 

    * Esse recurso consulta e nos retorna na resposta todos os sites e todos os hoteis atrelados a esse site.

####Exemplo de requisição:

    GET localhost:5000/sites

    Response: {
                "sites": [
                    {
                    "site_id": 1,
                    "url": "www.otelo.com.br",
                    "hotels": [
                        {
                        "hotel_id": 2,
                        "nome": "Free Hotel",
                        "city": "Santos",
                        "stars": 3.0,
                        "price": 230.0,
                        "site_id": 1
                        }
                    ]
                    }
                ]
            }

###Consultar um unico site /sites/:site_url:

    * Esse recurso nos retorna na resposta o site com a url passada na rota e os hoteis atrelados a esse site.

####Exemplo de requisição:

    GET localhost:5000/sites/www.otelo.com.br

    Response: { 
                "site_id": 1,
                "url": "www.otelo.com.br",
                "hotels": [
                    {
                    "hotel_id": 2,
                    "nome": "Free Hotel",
                    "city": "Santos",
                    "stars": 3.0,
                    "price": 230.0,
                    "site_id": 1
                    }
                ]
            } 

###Cadastrar um site /sites

    * Esse recurso é utilizado para cadastrar os sites, passamos no corpo da requisição o parametro url e tambem necessitamos estar autenticados.

####Exemplo de requisição:

    POST localhost:5000/sites

    Header: Authorization = Bearer "token de acesso" - precisamos antes do token ter a palavra "Bearer" para indentificar que estamos mandando um token e não um usuario e senha.

    Body: {
            "url": "urldosite"
        }

###Deletar um site /sites/:site_url

    * Esse recurso é para deletar um site, passamos a url do mesmo na rota e precisamos estar autenticados

####Exemplo de requisição:

    DELETE localhost:5000/sites/wwww.otelo.com.br

    Header: Authorization = Bearer "token de acesso" - precisamos antes do token ter a palavra "Bearer" para indentificar que estamos mandando um token e não um usuario e senha.

##Consultar Hotéis, criar, atualizar e deletar

###Consultar /hotels:

    *Requisição para listar todos os hotéis do sistema, podendo opcionalmente receber filtros personalizados via path, de forma que se o cliente não definir nenhum parâmetro de consulta (nenhum filtro), os parâmetros receberão os valores padrão. 

    * Possíveis parâmetros de consulta
        * city => Filtrar hotéis pela cidade escolhida. Padrão: Nulo 
        * stars_min => Avaliações mínimas de hotéis de 0 a 5. Padrão: 0
        * stars_max => Avaliações máximas de hotéis de 0 a 5. Padrão: 5
        * price_min => Valor mínimo da diária do hotel de R$ 0 a R$ 10.000,00. Padrão: 0
        * price_max => Valor máximo da diária do hotel de R$ 0 a R$ 10.000,00. Padrão: 10000
        * limit => Quantidade máxima de elementos exibidos por página. Padrão: 50
        * offset => Quantidade de elementos pular (geralmente múltiplo de limit). Padrão: 0

####Exemplo de requisição:

    GET localhost:5000/hotels - Retorna todos os hoteis, não necessita autenticação
    GET localhost:5000/hotels?city=Rio de Janeiro - Retorna apenas os hoteis cadastrados na cidade RJ
    GET localhost:5000/hotels?city=Rio de Janeiro&stars_min=4.3 - Retorna apenas os hoteis cadastrados na cidade RJ, com um minimo de 4.3 estrelas
    GET localhost:5000/hotels/:id - Retorna o hotel especifico com o id do parametro id

###Criar hoteis /hotels:

    * Para criar hoteis precisamos estar autenticados, e passar no body os seguintes parametros em json: name, city, stars, price e site_id, o hotel_id é gerado automaticamente pelo banco de dados.

####Exemplo de requisição:

    POST localhost:5000/hotels - mesma rota do get, porem com requisição post

    Header: Authorization = Bearer "token de acesso" - precisamos antes do token ter a palavra "Bearer" para indentificar que estamos mandando um token e não um usuario e senha.

    Body {
            "name" : "Home Hotel",
            "city" : "Santos",
            "stars" : 3.5,
            "price" : 280.00,
            "site_id": 5
        }

###Atualizar um hotel /hotels/id:

    * Para atualiar um hotel devemos estar autenticados, passar o hotel_id do mesmo na rota e no body os valores atualizados, não passamos o site_id, o site continua o mesmo. Como resposta recebemos o hotel com os dados atualizados.

####Exemplo de requisição:

    PUT localhost:5000/hotels/1 - passamos o id do hotel que queremos atualizar.

    Header: Authorization = Bearer "token de acesso" - precisamos antes do token ter a palavra "Bearer" para indentificar que estamos mandando um token e não um usuario e senha.

    Body {
            "name" : "Premium Hotel",
            "city" : "São paulo",
            "stars" : 4.5,
            "price" : 450.00,
        }

###Deletar um hotel /hotels/id:

    * Para deletar um hotel devemos estar autenticados e passar o id do mesmo na rota.

####Exemplo de requisição:

    DELETE localhost:5000/hotels/1 - passamos o id do hotel que queremos deletar.

    Header: Authorization = Bearer "token de acesso" - precisamos antes do token ter a palavra "Bearer" para indentificar que estamos mandando um token e não um usuario e senha.

