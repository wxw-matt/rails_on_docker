from jinja2 import Environment, FileSystemLoader, select_autoescape

def get_env(directory='templates'):
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape()
    )
    return env

def dc_rails_template(db, image_tag,  **kwargs):
    assert( db in ['postgres', 'mariadb', 'sqlite3'] )
    kwargs['image_tag'] = image_tag
    template = get_env().get_template('rails-%s-template.yml' % db)
    return template.render(**kwargs)

def dc_rails_postgres_template(image_tag, **kwargs):
    return dc_rails_template('postgres', image_tag, **kwargs)

def dc_rails_mariadb_template(image_tag, **kwargs):
    return dc_rails_template('mariadb', image_tag, **kwargs)

def dc_rails_sqlite3_template(image_tag, **kwargs):
    return dc_rails_template('sqlite3', image_tag, **kwargs)

def dc_postgres_config(db_host, app_name, dev_password='example'):
    template = get_env().get_template('pg-config-template.yml')
    return template.render(db_host=db_host, app_name=app_name, dev_password=dev_password)

def dc_mariadb_config(db_host, app_name, dev_password='example'):
    template = get_env().get_template('mariadb-config-template.yml')
    return template.render(db_host=db_host, app_name=app_name, dev_password=dev_password)

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
    print(dc_rails_postgres_template('myapp',networks=['rod-network']))
    print(dc_rails_mariadb_template('myapp',networks=['rod-network']))
    print(dc_rails_sqlite3_template('myapp',networks=['rod-network']))
    print(dc_postgres_config('rds','p9'))
