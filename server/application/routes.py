from controllers import api
import application

def routes(app):
    app.add_url_rule('/hello', view_func=api.hello)
    app.add_url_rule('/dashboard', view_func=api.dashboard)
    app.add_url_rule('/show-free-slots', view_func=api.available_slots, methods=['GET', 'POST'])
    app.add_url_rule('/book-appointment', view_func=api.book_appointment, methods=['GET', 'POST'])
    app.add_url_rule('/cancel-appointment', view_func=api.cancel_appointment, methods=['GET', 'POST'])