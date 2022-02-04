from jinja2 import Environment, FileSystemLoader, select_autoescape

def get_env(directory='templates'):
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape()
    )
    return env


def dc_rails_postgres_template(image_tag, rails_port="3000:3000", password="example",postgres_tag='',networks=["rod-network"]):
    template = get_env().get_template('rails-postgres-template.yml')
    return template.render(image_tag=image_tag,rails_port=rails_port, password=password, postgres_tag=postgres_tag, networks=networks)

def dc_rails_mariadb_template(image_tag, rails_port="3000:3000", password="example",mariadb_tag='',networks=["rod-network"]):
    template = get_env().get_template('rails-mariadb-template.yml')
    return template.render(image_tag=image_tag,rails_port=rails_port, password=password, mariadb_tag=mariadb_tag, networks=networks)


if __name__ == "__main__":
    # print(dc_rails_postgres_template('myapp',networks=['rod-network']))
    print(dc_rails_mariadb_template('myapp',networks=['rod-network']))
