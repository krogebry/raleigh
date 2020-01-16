#!/usr/bin/env python
import requests
import json
import sys
import boto3

project_name = sys.argv[1]
domain = "fqdn.com"


class KeyCloak:

    def __init__(self, domain, project_name):
        self.domain = domain
        self.project_name = project_name
        self.secrets = self.get_secrets()
        self.token = self.get_token()

    def headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"bearer {self.token}"
        }

    def get_secrets(self):
        sm_client = boto3.client("secretsmanager")
        return json.loads(
            sm_client.get_secret_value(SecretId=f"/company_name/projects/{project_name}/secrets/keycloak")["SecretString"])

    def get_url(self, path):
        return f"https://authn-{self.project_name}.{self.domain}{path}"

    def get_token(self):
        data = {
            "grant_type": "password",
            "scope": "openid",
            "username": "admin",
            "password": self.secrets["user"]["password"],
            "client_id": "admin-cli"}

        url = self.get_url("/auth/realms/master/protocol/openid-connect/token")
        response = requests.post(url, data=data)
        r_json = response.json()

        return r_json["access_token"]

    def get_client_json(self):
        client_json_file = open("etc/keycloak-clients.json")
        return json.loads(client_json_file.read())

    def make_clients(self):
        for client in self.get_client_json():
            url = self.get_url("/auth/admin/realms/master/clients")
            print(f"Creating user: {client['clientId']}")
            if client["clientId"] == "mgmt-api":
                client["secret"] = self.secrets["master_realm_secret"]

            response = requests.post(url, data=json.dumps(client), headers=self.headers())
            print(f"[{response.text}]")

    def get_roles(self):
        url = self.get_url("/auth/admin/realms/master/roles")
        response = requests.get(url, headers=self.headers())
        roles = response.json()
        for role in roles:
            print(role)

    def make_roles(self):
        roles = ["superadmin", "superuser", "tenantadmin", "tenantuser", "tenantreader"]
        url = self.get_url("/auth/admin/realms/master/roles")
        for role_name in roles:
            role_data = {"name": role_name}
            print(f"Creating role: {role_name}")
            response = requests.post(url, data=json.dumps(role_data), headers=self.headers())
            if response.status_code == 201:
                print("Role created")
            else:
                print(response.status_code)
                print(f"[{response.text}]")

    def get_clients(self):
        url = self.get_url("/auth/admin/realms/master/clients")
        response = requests.get(url, headers=self.headers())
        print(response.status_code)
        clients = response.json()
        for client in clients:
            print(f"{client['id']}\t{client['clientId']}")


if __name__ == "__main__":
    k = KeyCloak(domain, project_name)
    k.make_clients()
    # k.get_clients()

    k.make_roles()
    # k.get_roles()
