import os
import sys
from flask import Flask, jsonify, make_response, request, abort, render_template
from functools import wraps
import subprocess
import paramiko

app = Flask(__name__)

log = app.logger


key = paramiko.RSAKey.from_private_key_file('./.ssh/id_rsa')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy)


@app.errorhandler(412)
def version_mismatch(error):
    return 'Version mismatch. Expected: {}: {}.{}'.format(
        X_BROKER_API_VERSION_NAME,
        X_BROKER_API_MAJOR_VERSION,
        X_BROKER_API_MINOR_VERSION), 412


# Fonction principale appelant toutes les autres


@app.route('/dlkbroker', methods=['POST'])
def dlk_broker():
    fn = getattr(sys.modules['__main__'], '__file__')
    root_path = os.path.abspath(os.path.dirname(fn))
    user = request.form['user']
    site = request.form['site']
    env = request.form['env']
    if site in ('tls','qvi'):
        if env in ('dev', 'rct', 'prd'):
            # create_lu(root_path, user, site, env)
            create_kt(user)
            testparam(user, site, env, root_path)
            return 'OK'
        else :
            return 'L\'environnement ne peut être que <span style="font-weight:bold;color:blue">dev</span>, <span style="font-weight:bold;color:blue">rct</span> ou <span style="font-weight:bold;color:blue">qvi</span> en dehors de toute exeption'
    else:
        return 'Le site ne peut être que <span style="font-weight:bold;color:blue">tls</span> ou <span style="font-weight:bold;color:blue">qvi</span> en dehors de toute exeption'

# Fonction test parametre

def testparam(arg1, arg2, arg3, arg4):
    print(arg1, arg2, arg3, arg4)

def testOneparam(myParam):
    print(myParam)


# Fonction de creation de keytab

def create_kt(user):
    ktCmd = 'sudo /tech/local/bin/princ.sh '
    client.connect('qviqbkrbrs01', username='aosadm', pkey=key)
    ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(ktCmd + user)
    erre = ""
    for lineo in ssh_stdout:
        message = lineo
    for linee in ssh_stderr:
        erre = linee
    #pure_message = message.replace("\u001b[0;32;40mOK\u001b[m. ", "")
    returnCode = ssh_stdout.channel.recv_exit_status()
    returnCodeR = ssh_stderr.channel.recv_exit_status()
    kt_serv = {
        'message': message,
        'erreur': erre,
        'stdout code' : returnCode,
        'stderr code' : returnCodeR
    }
    client.close()
    return jsonify(kt_serv)




# ************** APPEL INDIVIDUEL DES FONCTIONS 

@app.route('/createkt')
def call_crKt():
    user = request.args.get('user')
    create_kt(user)
    return 'OK'




if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '9096')))