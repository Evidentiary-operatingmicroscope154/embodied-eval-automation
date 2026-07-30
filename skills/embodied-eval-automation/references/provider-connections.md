# Provider and source connections

Use the safest already-configured method. Prefer managed connectors or credential stores over copying credentials into commands.

## SSH and generic cloud servers

### Existing SSH key or agent

1. Ask for a redacted SSH command containing user, host, and port.
2. Inspect only public key names/fingerprints when needed; never print private-key content.
3. Verify the server host fingerprint through the cloud console, provider record, or trusted administrator.
4. Test a read-only command first.
5. Use strict host-key checking for unattended jobs.

### Password-only access

Ask the user to enter the password directly in an interactive terminal. Do not place it in command arguments, shell history, scripts, logs, chat, or environment files.

If unattended control is required:

1. Ask permission to create a dedicated, task-specific SSH key.
2. Store the private key in the user’s protected local SSH directory.
3. Show or copy only the public key.
4. Separately ask permission to add that public key to the named account’s `authorized_keys` or provider console.
5. Test read-only access and record the public-key fingerprint.
6. Document how the user can revoke the key.

### Provider CLI or managed identity

For AWS SSM, Google Cloud IAP/`gcloud compute ssh`, Azure Bastion/`az ssh`, Kubernetes, RunPod, or another provider:

- ask for provider, project/account, region, instance, and approved billing boundary;
- prefer an existing authenticated CLI session;
- inspect identity/status before login;
- do not create instances, modify IAM, open firewalls, or expand GPUs without separate approval;
- use the provider’s current official documentation rather than guessing commands.

## GitHub

Choose the least privileged route:

1. Existing GitHub connector/app when available.
2. Existing `gh` session; inspect with `gh auth status`.
3. Interactive `gh auth login`.
4. SSH using a local key whose public key is added to GitHub.

Ask whether the task needs:

- public read only;
- private repository read;
- issue/PR write;
- branch push;
- repository creation or release publication.

These are different authorization scopes. Never ask for a personal access token in chat. Do not put tokens in remote URLs. Git commits, pushes, PRs, releases, repository creation, and permission changes remain separate user approvals.

Official references:

- https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github
- https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account

## Hugging Face

Use:

1. Existing connector or cached authenticated session.
2. `hf auth whoami` to inspect status.
3. Interactive `hf auth login` or browser OAuth when needed.

Prefer read or fine-grained tokens for downloads. Use a write token only for an explicitly approved upload. Store the cache on the approved data volume.

Gated models require the user to accept or request access under their own account. Do not click acceptance, attest to a license, or submit personal information for the user without explicit authorization. After access is granted, pin the repository revision and record file sizes and hashes.

Official references:

- https://huggingface.co/docs/huggingface_hub/package_reference/authentication
- https://huggingface.co/docs/hub/security-tokens
- https://huggingface.co/docs/hub/models-gated

## Download fallback ladder

1. Test the canonical URL and a small range request.
2. Download remotely with resume, timeout, partial filenames, and hashes.
3. Use an approved mirror without changing version identity.
4. If remote transfer is too slow, ask permission for a user-controlled local download and upload.
5. Verify hashes again on the destination.

Changing source, version, or file is not a download workaround; it is a new artifact decision.
