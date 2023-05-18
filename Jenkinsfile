pipeline {
    agent {
        label 'kubernetes-docker-agent'
    }

    parameters {
        string(name: 'delay', defaultValue: '10', description: 'Delay between pod shutdown')
        string(name: 'namespace', defaultValue: 'default', description: 'Target namespace')
        string(name: 'timeout', defaultValue: '60', description: 'Timeout in seconds')
    }

    stages {
        stage('Create kube config file') {
            steps {
                withCredentials([vaultString(credentialsId: 'vault-kube-base64-config', variable: 'KUBECONFIG')]) {
                    writeFile file: 'config64', text: "$KUBECONFIG"
                }
                sh 'base64 --decode config64 > config && chmod 400 config && rm config64'
            }
        }

        stage('Run command') {
            steps {
                sh 'pip3 install -r requirements.txt'
                sh "python3 main.py --config config --delay ${params.delay} --namespace ${params.namespace} --timeout ${params.timeout}"
            }
        }
    }
}
