from reactors.utils import Reactor, agaveutils
import copy
import sys
import json
import os
import re


def submit_dicom(r, uploaded_file):
    # Create agave client from reactor object
    ag = r.client
    print(ag.systems.list())
    # copy our job.json from config.yml
    job_def = copy.copy(r.settings.dicom_reader)
    parameters = job_def["parameters"]
    # Define the input for the job as the file that
    # was sent in the notificaton message
    parameters["FILENAME"] = uploaded_file
    job_def.parameters = parameters
    site_file = os.path.normpath(uploaded_file).split('corral-secure/projects/A2CPS/submissions/')[-1]
    archivePath = job_def['archivePath'] + '/' + site_file.split('/')[0]
    job_def.name = site_file
    job_def.archivePath = archivePath


    notif = []

    job_def.notifications = notif

    # Submit the job in a try/except block
    try:
        # Submit the job and get the job ID
        job_id = ag.jobs.submit(body=job_def)['id']
        print(job_id)
        print(json.dumps(job_def, indent=4))
    except Exception as e:
        print(json.dumps(job_def, indent=4))
        print("Error submitting job: {}".format(e))
        print(e.response.content)
        return
    return

def message_vbr(r,filename,site,subject,session,zipfile,outdir):
    pipeline_config = copy.copy(r.settings.pipelines)
    vbr_actor_alias = pipeline_config['vbr_actor_alias']
    message = {
        "filename": dicoms,
        "site": site,
        "subject_id": subject,
        "session": session,
        "outdir": outdir
    }
    r.send_message(vbr_actor_alias, message)
    #r.send_message(actorId=vbr_actor_alias, message=message)
    return

def main():
    """Main function"""
    # create the reactor object
    r = Reactor()
    r.logger.info("Hello this is actor {}".format(r.uid))
    # pull in reactor context
    context = r.context
    #print(context)
    # get the message that was sent to the actor
    message = context.message_dict
    uploaded_file = message['uploaded_file']

    submit_dicom(r, uploaded_file)
    #message_vbr(r,site,subject,session,dicoms,outdir)
    return



if __name__ == '__main__':
    main()
