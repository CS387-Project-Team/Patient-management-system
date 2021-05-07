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

    #admin
    app.add_url_rule('/add-admin', view_func=api.add_admin, methods=['GET','POST'])
    app.add_url_rule('/add-remove-staff',view_func=api.add_remove_staff, methods=['GET'])
    app.add_url_rule('/add-doctor',view_func = api.add_doctor,methods=['POST'])
    app.add_url_rule('/add-staff',view_func=api.add_staff,methods=['POST'])
    app.add_url_rule('/remove-staff',view_func=api.remove_staff,methods=['POST'])
    app.add_url_rule('/upd-doctor',view_func=api.upd_doctor,methods=['POST'])
    app.add_url_rule('/upd-staff',view_func=api.upd_staff,methods=['POST'])
    app.add_url_rule('/view-resp',view_func=api.view_resp,methods=['GET'])
    app.add_url_rule('/assg-room-resp',view_func=api.assg_room_resp,methods=['POST'])
    app.add_url_rule('/assg-eqp-resp',view_func=api.assg_eqp_resp,methods=['POST'])
    app.add_url_rule('/evict-resp',view_func=api.evict_resp,methods=['POST'])

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

    app.add_url_rule('/dis_symp',view_func=api.view_dis_symp)
    app.add_url_rule('/add_disease', view_func=api.add_dis,methods=['POST'])
    app.add_url_rule('/add_symptom', view_func=api.add_symp,methods=['POST'])

    app.add_url_rule('/assign_room',view_func=api.assign_room, methods=['GET','POST'])

    # allot beds to admitted patients
    app.add_url_rule('/allot-beds', view_func=api.allot_beds, methods=['GET', 'POST'])
    app.add_url_rule('/allot-beds2', view_func=api.allot_beds2, methods=['GET', 'POST'])

    # update inventory
    app.add_url_rule('/update-inventory/add-bed', view_func=api.add_bed, methods=['GET', 'POST'])
    # app.add_url_rule('/update-inventory/remove-bed', view_func=api.remove_bed, methods=['GET', 'POST'])








