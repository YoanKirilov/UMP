from flask import Flask, render_template, request 
import psutil  
import speedtest  
import os  
import re  
import socket  

app = Flask(__name__)  # create Flask app instance

class Network_Details(object):
    def __init__(self):
        self.parser = psutil.net_if_addrs()  # get network interface addresses
        self.speed_parser = speedtest.Speedtest()  # create speed test instance
        self.interfaces = self.interface()[3]  # get list of network interfaces

    def interface(self):  # get all network interface names
        interfaces = []
        for interface_name, _ in self.parser.items():
            interfaces.append(str(interface_name))
        return interfaces
    
    def get_device_name(self, ip_address):  # get hostname for specified IP address
        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
            return hostname
        except socket.herror:
            return "Unknown"

    def scan_network(self):  # scan network for devices and return data about the host device
        response = os.popen("ping -n 1 192.168.0.0").read()  # ping the local network to get information about devices
        lines = response.split("\n")
        found_host = False  # initialize variable to track if host device is found
        for line in lines:
            match = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
            if match:
                ip_address = match.group(1)
                device_name = self.get_device_name(ip_address)
                if device_name == socket.gethostname():  # check if device name matches host device's hostname
                    return {"hostname": device_name, "ip_address": ip_address}
        return {"hostname": "Unknown", "ip_address": "Unknown"}

    def get_network_data(self, server_id=None):  # method to get network speed data and combine it with network interface and host device data
        if server_id:
            server = self.speed_parser.get_servers(server_id)[0]
            self.speed_parser.get_best_server(server)
        else:
            server = self.speed_parser.get_best_server()
        down = str(
            f"{round(self.speed_parser.download() / 1_000_000, 2)} Mbps")  # calculate download speed
        up = str(f"{round(self.speed_parser.upload() / 1_000_000, 2)} Mbps")  # calculate upload speed
        ping = str(f"{round(self.speed_parser.results.ping, 2)} ms")  # calculate ping
        interface = self.interfaces
        data = {"Interface Type:": [interface],
                "Download Speed:": [down],
                "Upload Speed:": [up],
                "Ping:": [ping],
                "Server:": [server['sponsor']]}  # create dictionary with all network data
        
        network_data = self.scan_network()
        data.update({"Hostname:": [network_data["hostname"]], "IP Address:": [network_data["ip_address"]]})  # add host device data to dictionary
        return data
    
@app.route('/', methods=['GET', 'POST'])  # specify route and allowed methods
def network_details():
    network = Network_Details() 
    if request.method == 'POST': 
        # retrieve server_id from form submission
        server_id = request.form.get('server_id')
        # call get_network_data method to retrieve network data and scan network for connected devices
        network_data = network.get_network_data(server_id)
        # retrieve server list for server dropdown menu
        servers = network.speed_parser.get_servers()
        # render HTML template with retrieved data and servers
        return render_template('network_details.html', network_data=network_data, servers=servers)
    else:
        return render_template('network_details.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
