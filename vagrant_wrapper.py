import vagrant
import os


def up_vm(vm_folder):
    v1 = vagrant.Vagrant(vm_folder)
    v1.up()


def halt_vm(vm_folder):
    v1 = vagrant.Vagrant(vm_folder)
    v1.halt()
    
    
def destroy_vm(vm_folder):
    v1 = vagrant.Vagrant(vm_folder)
    v1.destroy()


def status_vm(vm_folder):
    v1 = vagrant.Vagrant(vm_folder)
    print(v1.status())
    
    
def main():
    n = None
    
    
if __name__ == "__main__":
    main()