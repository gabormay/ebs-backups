import datetime
import boto3

def backup_handler(event, context):
    ec2 = boto3.resource('ec2')

    print "Starting scheduled EBS volume backup", datetime.datetime.now()
    i_backed_up = 0
    i_deleted = 0;

    # Process only volumes with the 'Backup' tag set (value is indifferent)
    # For each volume: 
    #   Create a fresh snapshot
    #   Cleanup earlier snapshots:
    #       Keep at least n_snapshots_to_keep backups
    #       Delete only ones older than min_snapshot_age_to_delete
    n_snapshots_to_keep = 3
    min_snapshot_age_to_delete = 0 # (in days)

    volumes_to_backup = ec2.volumes.filter(Filters=[{'Name': 'tag-key', 'Values': ['Backup']}])
    for vol in volumes_to_backup:
        # convenience dict of the volume's tags
        vol_tags = {t['Key']: t['Value'] for t in vol.tags}
        
        # Use the name of the volume as the base name for the snapshot if available
        # otherwise use the volume ID
        vol_name = vol_tags['Name'] if 'Name' in vol_tags else vol.id
        dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        
        # Submit the snapshot creation request
        print 'Backing up', vol.id, vol_name
        i_backed_up += 1
        snapshot = vol.create_snapshot(Description='Created by ebs-backup')
        
        # Add tags to the snapshot for later processing:
        # Name: for easier identification 
        # Backup: to signal that this was automatically created as a backup
        # Note that cleanup will only delete snapshot tagged as Backup
        sn_name = '{}-{}'.format(vol_name, dt)
        snapshot.create_tags(Tags=
        [
            {'Key': 'Name', 'Value': sn_name},
            {'Key': 'Backup', 'Value': 'true'}
        ])
        print 'Created snapshot', snapshot.id, sn_name

        # Now cleanup older backups
        backups = list(ec2.snapshots.filter(Filters=[{'Name': 'volume-id', 'Values': [vol.id]}]))
        for snap in sorted(backups, key=lambda s: s.start_time)[0:len(backups)-n_snapshots_to_keep]:
            if (datetime.date.today() - snap.start_time.date()).days >= min_snapshot_age_to_delete:
                print 'Deleting old snapshot', snap.id, snap.start_time, (datetime.date.today() - snap.start_time.date()).days, "days old"
                i_deleted += 1
                snap.delete()
                
    msg = "Done, created {} new backups and deleted {} old ones".format(i_backed_up, i_deleted)
    print msg
    return {'message': msg} 