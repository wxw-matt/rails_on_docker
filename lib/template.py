from jinja2 import Environment, FileSystemLoader, select_autoescape

def get_env(directory='templates'):
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape()
    )
    return env


def dc_rails_postgres_template(image_tag, rails_port="3000:3000", password="example",postgres_tag='',networks=["rod-network"]):
    template = get_env().get_template('rails-postgres-template.yml')
    return template.render(image_tag=image_tag, rails_port=rails_port, password=password, postgres_tag=postgres_tag, networks=networks)

def dc_rails_mariadb_template(image_tag, rails_port="3000:3000", password="example",mariadb_tag='', networks=["rod-network"]):
    template = get_env().get_template('rails-mariadb-template.yml')
    return template.render(image_tag=image_tag, rails_port=rails_port, password=password, mariadb_tag=mariadb_tag, networks=networks)

def dc_rails_sqlite3_template(image_tag, rails_port="3000:3000",networks=["rod-network"]):
    template = get_env().get_template('rails-sqlite3-template.yml')
    return template.render(image_tag=image_tag, rails_port="3000:3000", networks=networks)

def dc_postgres_config(db_host, app_name):
    template = get_env().get_template('pg-config-template.yml')
    return template.render(db_host=db_host, app_name=app_name)

def dc_mariadb_config(db_host, app_name):
    template = get_env().get_template('mariadb-config-template.yml')
    return template.render(db_host=db_host, app_name=app_name)

def dockerfile_template(image_tag):
    dockerfile_template = f"""
FROM {image_tag}

RUN mkdir -p /app
ENV HOME /app
COPY Gemfile Gemfile.lock ./
RUN bundle install
"""
    return dockerfile_template



if __name__ == "__main__":
    # print(dc_rails_postgres_template('myapp',networks=['rod-network']))
    # print(dc_rails_mariadb_template('myapp',networks=['rod-network']))
    print(dc_postgres_config('rds','p9'))
