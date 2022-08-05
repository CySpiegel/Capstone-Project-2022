# Python built-in
import socket
import subprocess

# Third party
import paramiko



def ssh_connect(dst_node_ip, port=22, username="root", password="", ssh_obj=None, timeout=1, **kwargs):
    """
    Creates an ssh connection between two nodes. The object returned can be used
    as a reference to the SSH connection and treated just as a regular ssh
    connection on a terminal. This command also supports ssh pivoting.
    Simply pass the previous ssh object in the parameters and all traffic will be
    tunneled through the current ssh session into the future one.
    :param dst_node_ip: The IP of the destination node
    :type dst_node_ip: str
    :param port: The open port of IP address
    :type port: int
    :param username: The username to connect with
    :type username: str
    :param ssh_obj: A high-level representation of a session with an SSH server.
    :type ssh_obj: paramiko.client.SSHClient
    :param: \**kwargs: Additional keyword arguments which can be passed into the
                       paramiko.client.SSHClient.connect
                       (http://docs.paramiko.org/en/2.2/api/client.html#paramiko.client.SSHClient.connect).
                       If no argument is given, the connect will automatically
                       check the users `~/.ssh/` for `id_rsa`, `id_dsa`, etc.
    :rtype: paramiko.client.SSHClient or None
    :return: The SSH connection object or None if the connection fails
    :Example 1:
    # initial ssh connection from base host
    >> connect("localhost", "test", password="test")
    >> connect("localhost", "test", key_filename="~/.ssh/id_rsa")
    :Example 2:
    # ssh pivoting after initial ssh connection (previous connect created ssh_obj1)
    >> connect("10.2.1.17", 53, "root", ssh_obj1, password="")
    >> connect("10.2.1.6", "root", ssh_obj2, key_filename="~/.ssh/id_rsa")
    """
    # Check if ssh_obj is given for ssh pivoting
    if ssh_obj is not None:
        # Obtain ssh_object host IP
        current_host = ssh_obj.get_transport().sock.getpeername()[0]

        # Create tunnel through the given ssh_obj
        new_tunnel = create_traffic_tunnel(ssh_obj, dst_node_ip, current_host)
    try:
        ssh_obj2 = paramiko.SSHClient()
        ssh_obj2.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if ssh_obj is not None:
            ssh_obj2.connect(dst_node_ip, port=port, username=username, password=password, sock=new_tunnel, timeout=timeout, **kwargs)
        else:    
            ssh_obj2.connect(dst_node_ip, port=port, username=username, password=password, timeout=timeout, **kwargs)
        return ssh_obj2

    except paramiko.ssh_exception.AuthenticationException as ssh_error:
        print(
            "Paramiko cannot connect to the given node."
            "Error given: {}".format(ssh_error.args[0])
        )
    return None


def send_command(ssh_obj, command, **kwargs):
    """
    Running an SSH command on the remote box specified by ssh_obj.

    :param ssh_obj: The SSH connection object.
    :type ssh_obj: paramiko.client.SSHClient
    :param command: The command to run on the remote box.
    :type command: str

    :returns: The program's exit code followed by a list of each line of stdout
              or stderr if the exit code is 0 or >= 1, respectively.
    :rtype: tuple
    """
    stdin, stdout, stderr = ssh_obj.exec_command(command, **kwargs)
    exit_code = stdout.channel.recv_exit_status()

    if exit_code == 0:
        return exit_code, [x.rstrip() for x in stdout.readlines()]
    else:
        return exit_code, [x.rstrip() for x in stderr.readlines()]


def send_interactive_command(ssh_obj, command, inputs, **kwargs):
    """
    Running an SSH command on the remote box specified by ssh_obj that requires
    some form of user interaction such as sudo.

    :param ssh_obj: The SSH connection object.
    :type ssh_obj: paramiko.client.SSHClient
    :param command: The command to run on the remote box.
    :type command: str
    :param inputs: The list of strings the user must write to the terminal in
                   sequential order.
    :type inputs: list

    :returns: The program's exit code followed by a list of each line of stdout
              or stderr if the exit code is 0 or >= 1, respectively.
    :rtype: tuple

    :Raises socket.timeout: If the command times out.

    ..codeblock:: bash
        # Think of this command as doing this
        >> sudo ls
        [sudo] password for <user>: inputs[0]
        ...stdout...

    ..notes::
        The command will timeout if an improper or incorrect list of inputs is
        provided such as an incorrect password for sudo.
    """
    kwargs.setdefault("timeout", 5)

    stdin, stdout, stderr = ssh_obj.exec_command(
        command,
        get_pty=True,
        **kwargs
    )

    for user_input in inputs:
        stdin.write("{}\n".format(user_input))
    stdin.flush()

    try:
        console_output = [x.rstrip() for x in stdout.readlines()]
        console_error = [x.rstrip() for x in stderr.readlines()]
        exit_code = stdout.channel.recv_exit_status()

        if exit_code == 0:
            return (exit_code, console_output)
        else:
            return (exit_code, console_error)

    except socket.timeout as timeout_error:
        raise socket.timeout


def end_session(ssh_obj):
    """
    Executes logging out for the ssh_obj session.

    :param ssh_obj: The SSH connection object
    :type ssh_obj: paramiko.client.SSHClient

    :returns: True if the logout occurred successfully; otherwise, False.
    :rtype: True or False
    """
    try:
        ssh_obj.close()
        return True
    except paramiko.ssh_exception.SSHException:
        return False

