'''

VM Volumes operations for test.

@author: Youyk
'''

import apibinding.api_actions as api_actions
import zstackwoodpecker.test_util as test_util
import apibinding.inventory as inventory
import account_operations

def create_volume_from_offering(volume_option):
    action = api_actions.CreateDataVolumeAction()
    action.diskOfferingUuid = volume_option.get_disk_offering_uuid()
    action.description = volume_option.get_description()
    timeout = volume_option.get_timeout()
    if not timeout:
        action.timeout = 240000
    else:
        action.timeout = timeout

    name = volume_option.get_name()
    if not name:
        action.name = 'test_volume'
    else:
        action.name = name

    test_util.action_logger('Create [Volume:] %s with [disk offering:] %s ' % (action.name, action.diskOfferingUuid))
    evt = account_operations.execute_action_with_session(action, volume_option.get_session_uuid())

    test_util.test_logger('[volume:] %s is created.' % evt.inventory.uuid)
    return evt.inventory

def create_volume_template(volume_uuid, backup_storage_uuid_list, name = None, \
        session_uuid = None):
    action = api_actions.CreateDataVolumeTemplateFromVolumeAction()
    action.volumeUuid = volume_uuid
    if name:
        action.name = name
    else:
        action.name = 'new_template_from_volume_%s' % volume_uuid

    action.backupStorageUuids = backup_storage_uuid_list
    test_util.action_logger('Create [Volume Template] for [Volume:] %s on [Backup Storages:] %s' % (volume_uuid, backup_storage_uuid_list))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    test_util.test_logger('[Volume Templated:] %s is created.' % evt.inventory.uuid)
    return evt.inventory

def create_volume_from_template(image_uuid, ps_uuid, name = None, \
        host_uuid = None, session_uuid = None):
    action = api_actions.CreateDataVolumeFromVolumeTemplateAction()
    action.imageUuid = image_uuid
    action.primaryStorageUuid = ps_uuid
    if name:
        action.name = name
    else:
        action.name = 'new volume from template %s' % image_uuid

    if host_uuid:
        action.hostUuid = host_uuid

    evt = account_operations.execute_action_with_session(action, session_uuid)
    test_util.test_logger('[Volume:] %s is created from [Volume Template:] %s on [Primary Storage:] %s.' % (evt.inventory.uuid, image_uuid, ps_uuid))
    return evt.inventory

def delete_volume(volume_uuid, session_uuid=None):
    action = api_actions.DeleteDataVolumeAction()
    action.uuid = volume_uuid
    action.timeout = 240000
    evt = account_operations.execute_action_with_session(action, session_uuid)
    test_util.action_logger('Delete Volume [uuid:] %s' % volume_uuid)
    return evt.inventory

def expunge_volume(volume_uuid, session_uuid=None):
    action = api_actions.ExpungeDataVolumeAction()
    action.uuid = volume_uuid
    action.timeout = 60000
    evt = account_operations.execute_action_with_session(action, session_uuid)
    test_util.action_logger('Expunge Volume [uuid:] %s' % volume_uuid)
    return evt

def attach_volume(volume_uuid, vm_uuid, session_uuid=None):
    action = api_actions.AttachDataVolumeToVmAction()
    action.vmInstanceUuid = vm_uuid
    action.volumeUuid = volume_uuid
    action.timeout = 240000
    test_util.action_logger('Attach Data Volume [uuid:] %s to [vm:] %s' % (volume_uuid, vm_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt.inventory

def detach_volume(volume_uuid, session_uuid=None):
    action = api_actions.DetachDataVolumeFromVmAction()
    action.uuid = volume_uuid
    action.timeout = 240000
    test_util.action_logger('Detach Volume [uuid:] %s' % volume_uuid)
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt.inventory

def create_snapshot(snapshot_option, session_uuid=None):
    action = api_actions.CreateVolumeSnapshotAction()
    action.volumeUuid = snapshot_option.get_volume_uuid()
    action.name = snapshot_option.get_name()
    if not action.name:
        action.name = 'snapshot_for_volume_%s' % action.volumeUuid
    action.description = snapshot_option.get_description()
    action.timeout = 240000
    if snapshot_option.get_session_uuid():
        session_uuid = snapshot_option.get_session_uuid()
    evt = account_operations.execute_action_with_session(action, session_uuid)
    snapshot = evt.inventory
    test_util.action_logger('Create [Snapshot:] %s [uuid:] %s for [volume:] %s' % \
            (action.name, snapshot.uuid, action.volumeUuid))
    return snapshot

def create_snapshot_scheduler(snapshot_option, type, name, start_time=None, interval=None, repeatCount=None, cron=None, session_uuid=None):
    action = api_actions.CreateVolumeSnapshotSchedulerAction()
    action.volumeUuid = snapshot_option.get_volume_uuid()
    action.snapShotName = snapshot_option.get_name()
    if not action.snapShotName:
        action.snapShotName = 'scheduler_snapshot_for_volume_%s' % action.volumeUuid
    action.description = snapshot_option.get_description()
    action.type = type
    action.schedulerName = name
    action.startTime = start_time
    action.interval = interval
    action.repeatCount = repeatCount
    action.cron = cron
    action.timeout = 240000
    if snapshot_option.get_session_uuid():
        session_uuid = snapshot_option.get_session_uuid()
    evt = account_operations.execute_action_with_session(action, session_uuid)
    snapshot = evt.inventory
    test_util.action_logger('Scheduler Create [Snapshot:] %s for [volume:] %s [type:] %s [startTime:] %s [interval:] %s [repeatCount:] %s [cron:] %s' % \
            (action.snapShotName, action.volumeUuid, type, start_time, interval, repeatCount, cron))
    return snapshot

def delete_snapshot(snapshot_uuid, session_uuid=None):
    action = api_actions.DeleteVolumeSnapshotAction()
    action.uuid = snapshot_uuid
    action.timeout = 240000
    test_util.action_logger('Delete [Snapshot:] %s ' % snapshot_uuid)
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt

def use_snapshot(snapshot_uuid, session_uuid=None):
    action = api_actions.RevertVolumeFromSnapshotAction()
    action.uuid = snapshot_uuid
    action.timeout = 24000
    test_util.action_logger('Revert Volume by [Snapshot:] %s ' % snapshot_uuid)
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt

def backup_snapshot(snapshot_uuid, backup_storage_uuid=None, session_uuid=None):
    action = api_actions.BackupVolumeSnapshotAction()
    action.uuid = snapshot_uuid
    action.backupStorageUuid = backup_storage_uuid
    evt = account_operations.execute_action_with_session(action, session_uuid)
    snapshot = evt.inventory
    test_util.action_logger('Backup [Snapshot:] %s to [bs]: %s ' \
            % (snapshot_uuid,\
            snapshot.backupStorageRefs[0].backupStorageUuid))
    return snapshot

def delete_snapshot_from_backupstorage(snapshot_uuid, bs_list=[], \
        delete_mode=None, session_uuid=None):
    action = api_actions.DeleteVolumeSnapshotFromBackupStorageAction()
    action.uuid = snapshot_uuid
    action.backupStorageUuids = bs_list
    action.deleteMode = delete_mode
    action.timeout = 24000
    test_util.action_logger('Delete [Snapshot:] %s from backup storage: %s' \
            % (snapshot_uuid, bs_list))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt

def create_volume_from_snapshot(snapshot_uuid, name=None, ps_uuid=None, \
        session_uuid=None):
    action = api_actions.CreateDataVolumeFromVolumeSnapshotAction()
    if name:
        action.name = name
    else:
        action.name = 'create_volume_from_snapshot'

    action.primaryStorageUuid = ps_uuid
    action.volumeSnapshotUuid = snapshot_uuid
    evt = account_operations.execute_action_with_session(action, session_uuid)
    volume = evt.inventory
    test_util.action_logger('[Volume:] %s is created from [snapshot]: %s on \
[primary storage:] %s' % (volume.uuid, snapshot_uuid, \
            volume.primaryStorageUuid))
    return volume

def create_volume_offering(disk_offering_option, \
        session_uuid=None):
    action = api_actions.CreateDiskOfferingAction()
    action.diskSize = disk_offering_option.get_diskSize()
    action.name = disk_offering_option.get_name()
    action.description = disk_offering_option.get_description()
    action.allocatorStrategy = disk_offering_option.get_allocatorStrategy()
    test_util.action_logger('Create disk offering: name: %s, diskSize: %d' \
            % (action.name, action.diskSize))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    test_util.test_logger('Disk Offering: %s is created' % evt.inventory.uuid)
    return evt.inventory

def delete_disk_offering(disk_offering_uuid, session_uuid = None):
    action = api_actions.DeleteDiskOfferingAction()
    action.uuid = disk_offering_uuid
    test_util.action_logger('Delete Disk Offering [uuid:] %s' \
            % disk_offering_uuid)
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt

def get_local_storage_capacity(host_uuid, primary_storage_uuid, \
        session_uuid = None):
    '''
        If host_uuid is None, it will return a list of capacity for every Hosts.
    '''
    action = api_actions.GetLocalStorageHostDiskCapacityAction()
    action.hostUuid = host_uuid
    action.primaryStorageUuid = primary_storage_uuid
    test_util.action_logger('Get Local Storage Capacity for host: %s, primary storage: %s' \
            % (host_uuid, primary_storage_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt.inventories

def migrate_volume(volume_uuid, host_uuid, session_uuid = None):
    action = api_actions.LocalStorageMigrateVolumeAction()
    action.destHostUuid = host_uuid
    action.volumeUuid = volume_uuid
    test_util.action_logger('Migrate Local Storage Volume: %s to Host: %s' \
            % (volume_uuid, host_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)

def get_volume_migratable_host(volume_uuid, session_uuid = None):
    action = api_actions.LocalStorageGetVolumeMigratableHostsAction()
    action.volumeUuid = volume_uuid
    test_util.action_logger('Get Volume: %s Migratable Volume for Local Storage:' % volume_uuid)
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt.inventories
