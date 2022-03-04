from jinja2 import Environment, FileSystemLoader, select_autoescape

def get_env(directory='templates'):
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape()
    )
    return env

def dc_rails_template(db, image_tag,  **kwargs):
    assert( db in ['postgres', 'mariadb', 'sqlite3'] )
    if image_tag:
        image_tag = image_tag.replace('_', '-')
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

def dc_sqlite3_template(db_host, app_name, dev_password='example'):
    template = get_env().get_template('sqlite3-config-template.yml')
    return template.render(db_host=db_host, app_name=app_name, dev_password=dev_password)

# replicas, app_name, created_at
def k8s_deployment_template(image_tag, **kwargs):
    if image_tag:
        image_tag = image_tag.replace('_', '-')
    kwargs['image_tag'] = image_tag
    template = get_env().get_template('k8s-deployment-template.yml')
    return template.render(**kwargs)

# app_name, port
def k8s_service_template(app_name, **kwargs):
    if app_name:
        app_name = app_name.replace('_', '-')
    kwargs['app_name'] = app_name
    template = get_env().get_template('k8s-service-template.yml')
    return template.render(**kwargs)

def dockerfile_pro_template(rails_base_tag, **kwargs):
    kwargs['rails_base_tag'] = rails_base_tag
    template = get_env().get_template('Dockerfile-pro-template')
    return template.render(**kwargs)

def dockerfile_template(rails_base_tag):
    dockerfile_template = f"""
FROM {rails_base_tag}

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
