FROM 736487896839.dkr.ecr.eu-west-2.amazonaws.com/mattermost-integration-testing:1
RUN mattermost -c /mm/mattermost/config/config_docker.json config set ServiceSettings.AllowedUntrustedInternalConnections "127.0.0.1 0.0.0.0 localhost ::1"
