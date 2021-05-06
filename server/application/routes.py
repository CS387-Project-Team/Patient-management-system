from controllers import api
import application

def routes(app):
    app.add_url_rule('/hello', view_func=api.hello)
    # dash
    app.add_url_rule('/dashboard', view_func=api.dashboard)

    # history
    app.add_url_rule('/view-history', view_func=api.view_history, methods=['GET'])
    app.add_url_rule('/edit-history', view_func=api.add_history, methods=['GET', 'POST'])
    app.add_url_rule('/delete-history', view_func=api.delete_history, methods=['POST'])
    app.add_url_rule('/update-history', view_func=api.update_history, methods=['POST'])

    # appos
    app.add_url_rule('/appointments', view_func=api.get_appointments)
    app.add_url_rule('/show-free-slots', view_func=api.available_slots, methods=['GET'])
    app.add_url_rule('/show-free-slots-followup', view_func=api.available_slots_followup, methods=['GET'])
    app.add_url_rule('/update-date-free-slots', view_func=api.update_date_free_slots, methods=['POST'])
    app.add_url_rule('/update-date-free-slots-followup', view_func=api.update_date_free_slots_followup, methods=['POST'])
    # app.add_url_rule('/confirm-booking', view_func=api.confirm_appointment_post, methods=['POST'])
    # app.add_url_rule('/confirm-booking', view_func=api.confirm_appointment_get, methods=['GET'])
    app.add_url_rule('/book-appointment', view_func=api.book_appointment, methods=['GET', 'POST'])
    app.add_url_rule('/cancel-appointment', view_func=api.cancel_appointment, methods=['GET', 'POST'])
    app.add_url_rule('/update-complaint', view_func=api.update_complaint, methods=['POST'])

    # view general info
    app.add_url_rule('/view-info',view_func=api.view_info,methods=['GET'])

    # my profile
    app.add_url_rule('/my-profile',view_func=api.profile,methods=['GET', 'POST'])

    # analytics
    app.add_url_rule('/analytics-data',view_func=api.get_analytics,methods=['GET'])
    app.add_url_rule('/analytics',view_func=api.show_analytics,methods=['GET'])
    app.add_url_rule('/analytics-disease-data/<int:disease_id>',view_func=api.get_disease_analytics,methods=['GET'])
    app.add_url_rule('/analytics-disease/<int:disease_id>',view_func=api.show_disease_analytics,methods=['GET'])
    app.add_url_rule('/analytics-disease-post',view_func=api.post_disease_for_analytics,methods=['POST'])

    ## tests
    app.add_url_rule('/tests', view_func=api.get_tests)
    app.add_url_rule('/book_test', view_func=api.book_test, methods=['GET', 'POST'])
    app.add_url_rule('/available_tests', view_func=api.available_tests, methods=['GET'])
    app.add_url_rule('/cancel_test', view_func=api.cancel_test, methods=['GET', 'POST'])

    # administer tests
    app.add_url_rule('/administer_test', view_func=api.administer_test, methods=['GET', 'POST'])









