from private import authorization, config
import parser
import sql as bd

if __name__ == '__main__':

    # susu = parser.pars()
    # susu.get_authorization(authorization.login, authorization.password)
    # susu.enter_to_schedule()
    # susu.enter_to_start_of_semester()

    sql = bd.MySql(config.host, config.user, config.password, config.db_name)
    # sql.delete_all_from_db()

    # susu.schedule_to_db(sql)

    sql.get_day_schedule('19.05')
    # sql.output_db()
    sql.connection.close()


