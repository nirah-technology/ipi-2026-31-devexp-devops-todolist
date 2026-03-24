pipeline {
    agent {
        docker {
            image 'python:3.14'
            // On monte le socket pour que le conteneur Python puisse piloter le moteur de l'hôte
            args '-u root:root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    stages {
        stage("Install Docker CLI") {
            steps {
                sh '''
                    apt-get update && apt-get install -y ca-certificates curl
                    install -m 0755 -d /etc/apt/keyrings
                    curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
                    chmod a+r /etc/apt/keyrings/docker.asc

                    # Configuration propre du dépôt Docker pour Debian Trixie (utilisé par l'image python:3.14)
                    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian bookworm stable" > /etc/apt/sources.list.d/docker.list
                    
                    apt-get update && apt-get install -y docker-ce-cli
                '''
                // Vérification immédiate
                sh 'docker --version'
            }
        }
        stage("Checkout") {
            steps {
                git credentialsId: 'jenkins-github-key', branch: 'main', url: 'git@github.com:nirah-technology/ipi-2026-31-devexp-devops-todolist.git'
            }
        }
        stage("Build & Dockerize") {
            steps {
                sh '''
                    python -m pip install poetry
                    poetry install
                    poetry build
                    docker build -t todolist:latest .
                '''
            }
        }
    }
}
