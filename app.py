from shiny import App, reactive, ui, render
from user_auth import user_sign_up

app_ui = ui.page_fluid(
    ui.input_text('email','E-mail'),
    ui.input_text('password','Password'),
    ui.input_action_button('signup','Signup')
)


def server(input):
    
    @reactive.event(input.signup)
    def george():
        user_sign_up('Hello', 'wodl')


app = App(app_ui, server)