import boto3


def print_environment_variables_for_all_apps():
    client = boto3.client('elasticbeanstalk')
    apps = client.describe_applications()

    # print([x['ApplicationName'] for x in apps['Applications']])
    application_names = [x['ApplicationName'] for x in apps['Applications']]

    for application in application_names:
        environemnts = client.describe_environments(ApplicationName=application)
        environment_names = [x['EnvironmentName'] for x in environemnts['Environments']]
        for environment_name in environment_names:
            settings = client.describe_configuration_settings(ApplicationName=application, EnvironmentName=environment_name)
            option_settings = settings['ConfigurationSettings'][0]['OptionSettings']
            environment_settings = [x for x in option_settings if x['OptionName'] == 'EnvironmentVariables']
            if 'Value' not in environment_settings[0].keys():
                continue
            env_vars = environment_settings[0]['Value']
            environment_variables_for_appenv = dict([tuple(x.split('=', 1)) for x in env_vars.split(',')])

            first_line = True
            for i, v in environment_variables_for_appenv.items():
                output = "{}\t{}\t{}={}"
                if first_line == True:
                    output = output.format(application, environment_name, i, v)
                    first_line = False
                else:
                    output = output.format('','', i, v)
                print(output)


if __name__ =='__main__':
    print_environment_variables_for_all_apps()
