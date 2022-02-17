from dash import Dash, html, dcc, Output, Input, State;
import dash_bootstrap_components as dbc

from main import InstgrameProfile_Scrapper

app = Dash(__name__)
islogin = False;
bot = 0;

app.layout = html.Div(children=[
    html.Header(children=[
        html.H1("INSTAGRAM BOT"),
        html.H3("created By Grich")
    ]
        , id='header_box'
    ),
    html.Section(
        children=[
            html.Div(
                id='login_cri',
                children=[
                    html.Div(children=[html.H2(
                        '-> Login Info :'
                    ),
                    ]),
                    html.Div(
                        id='input_box',
                        children=[
                            html.Div(
                                className='alert_Box'
                                , id='login_output'
                            ),
                            dcc.Input(
                                id='username',
                                placeholder="username",
                                type='text'

                            ), dcc.Input(
                                id='password',
                                placeholder="password",
                                type='text'

                            )
                        ]
                    ),
                    html.Div(
                        id='box_te',
                        children=[html.Button(
                            id='login_button',
                            n_clicks=0,
                            children='Login'
                        )]),

                ]
            ),
            html.Div(
                id='scraper_cri',
                children=[
                    html.Div(children=[html.H2(
                        '-> Scraper Bot :'
                    ),
                    ]),

                    html.Div(
                        id='input_box_scraper',
                        children=[
                            html.Div(
                                className='alert_Box'
                                , id='scraper_output'
                            ),
                            dcc.Input(
                                id='username_Scraped',
                                placeholder="username Scraper",
                                type='text'

                            ),
                        ]
                    ),
                    html.Div(
                        id='box_te_scraper',
                        children=[html.Button(
                            id='Scraper_button',
                            n_clicks=0,
                            children='Scrape'
                        )]),

                ]
            ),
            html.Div(
                id='tags_cri',
                children=[
                    html.Div(children=[html.H2(
                        '-> Tags Bot :'
                    ),
                    ]),

                    html.Div(
                        id='input_box_tags',
                        children=[
                            html.Div(
                                className='alert_Box'
                                , id='tags_output'
                            ),
                            dcc.Input(
                                id='tags_post_url',
                                placeholder="Post url",
                                type='text'

                            ),
                            dcc.Input(
                                id='tags_post_data',
                                placeholder="url Of usrnames",
                                type='text'

                            )]
                    ),
                    html.Div(
                        id='box_te_tags',
                        children=[html.Button(
                            id='tags_button',
                            children='Tag',
                            n_clicks=0,

                        )]),

                ]
            ), html.Div(
                id='msg_cri',
                children=[
                    html.Div(children=[html.H2(
                        '-> Messaging bot :'
                    ),
                    ]),

                    html.Div(

                        id='input_box_msg',
                        children=[
                            html.Div(
                                className='alert_Box'
                                , id='msg_output'
                            ),
                            dcc.Input(
                                id='msg_post_data',
                                placeholder="url Of usrnames",
                                type='text'

                            )]
                    ),
                    html.Div(
                        id='box_te_msg',
                        children=[html.Button(
                            id='msg_button',
                            children='Start',
                            n_clicks=0,
                        )]),
                ]
            )
        ]
    )
])


@app.callback(
    Output('login_output', 'children'),
    Input('login_button', 'n_clicks'),
    State('username', 'value'),
    State('password', 'value'))
def login(n_clicks, username, password, ):
    print('------------->n_click login=' + str(n_clicks))
    if n_clicks != 0:
        global bot;
        global islogin
        bot = InstgrameProfile_Scrapper();
        i = bot.login(username, password);
        if i == 1:
            islogin = True
            return 'Login Suc'
        else:
            return 'Login Error'


@app.callback(
    Output('scraper_output', 'children'),
    Input('Scraper_button', 'n_clicks'),
    State('username_Scraped', 'value'))
def scraper(n_clicks, username):
    global islogin
    if islogin == True:
        print('------------->n_click scarpper=' + str(n_clicks))
        username = [username]
        print(type(username))
        if n_clicks != 0:
            global bot;
            i = bot.get_followers(username, 30);
            if i == 1:
                return 'Scraping Don !'
            else:
                return 'Error while Scraping'
    else:
        return 'please Login first !'


@app.callback(
    Output('tags_output', 'children'),
    Input('tags_button', 'n_clicks'),
    State('tags_post_data', 'value'),
    State('tags_post_url', 'value'), )
def postTags(n_clicks, data_url, url):
    global islogin;
    if islogin == True:
        print('------------->n_click tags=' + str(n_clicks))
        if n_clicks != 0:
            global bot;
            i = bot.load_post(url, data_url);
            if i == 1:
                return 'Done'
            else:
                return 'Error'
    else:
        return 'please Login !'


@app.callback(
    Output('msg_output', 'children'),
    Input('msg_button', 'n_clicks'),
    State('msg_post_data', 'value'), )
def Messaging(n_clicks, data_url):
    global islogin
    if islogin == True:
        print('------------->n_click tags=' + str(n_clicks))
        if n_clicks != 0:
            global bot;
            i = bot.post_mesg_to_group(data_url);
            if i == 1:
                return 'Done'
            else:
                return 'Error'
    else:
        return 'Please Login !'


if __name__ == '__main__':
    app.run_server(debug=True)
