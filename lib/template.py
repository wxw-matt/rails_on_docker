from jinja2 import Environment, FileSystemLoader, select_autoescape

def get_env(directory='templates'):
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape()
    )
    return env

def template_render(template_file, **kwargs):
    template = get_env().get_template(template_file)
    return template.render(**kwargs)

def dc_rails_template(db, image_tag,  **kwargs):
    assert( db in ['postgres', 'mariadb', 'sqlite3'] )
    if image_tag:
        image_tag = image_tag.replace('_', '-')
    kwargs['image_tag'] = image_tag
    return template_render('rails/docker-compose-%s-template.yml' % db, **kwargs)

def dc_rails_postgres_template(image_tag, **kwargs):
    return dc_rails_template('postgres', image_tag, **kwargs)

def dc_rails_mariadb_template(image_tag, **kwargs):
    return dc_rails_template('mariadb', image_tag, **kwargs)

def dc_rails_sqlite3_template(image_tag, **kwargs):
    return dc_rails_template('sqlite3', image_tag, **kwargs)

def rails_database_config(template_file, db_host, app_name, dev_password='example'):
    kwargs = dict(db_host=db_host, app_name=app_name, dev_password=dev_password)
    return template_render(template_file, **kwargs)

def dc_postgres_config(db_host, app_name, dev_password='example'):
    return rails_database_config('rails/pg-config-template.yml', db_host, app_name, dev_password)

def dc_mariadb_config(db_host, app_name, dev_password='example'):
    return rails_database_config('rails/mariadb-config-template.yml', db_host, app_name, dev_password)

def dc_sqlite3_template(db_host, app_name, dev_password='example'):
    return rails_database_config('rails/sqlite3-config-template.yml', db_host, app_name, dev_password)

def dockerfile_pro_template(rails_base_tag, **kwargs):
    kwargs['rails_base_tag'] = rails_base_tag
    return template_render('rails/Dockerfile-pro-template', **kwargs)

def dockerfile_dev_template(rails_base_tag):
    kwargs = {'rails_base_tag':  rails_base_tag}
    return template_render('rails/Dockerfile-dev-template', **kwargs)


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


if __name__ == "__main__":
    print(dc_rails_postgres_template('myapp',networks=['rod-network']))
    print(dc_rails_mariadb_template('myapp',networks=['rod-network']))
    print(dc_rails_sqlite3_template('myapp',networks=['rod-network']))
    print(dc_postgres_config('rds','p9'))
