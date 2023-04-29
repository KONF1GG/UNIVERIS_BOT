from private import authorization, config
import parser
import sql as bd

if __name__ == '__main__':

    susu = parser.pars()
    susu.get_authorization(authorization.login, authorization.password)
    susu.enter_to_schedule()

    sql = bd.MySql(config.host, config.user, config.password, config.db_name)
    susu.schedule_to_db(sql)
    sql.output_db()
    sql.connection.close()


