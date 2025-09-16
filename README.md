
# Clarity Smart Contract Development Automation Suite

A comprehensive collection of Bash automation scripts designed to streamline the entire development workflow for Clarity smart contracts on the Stacks blockchain within the Replit IDE environment. This suite eliminates repetitive setup tasks and standardizes development practices across Clarity projects.

---

## 🎯 Overview

The Clarity Automation Suite provides a complete end-to-end solution for Clarity smart contract development, from initial project scaffolding to daily development workflows. Built specifically for Replit environments, these scripts integrate seamlessly with Clarinet, Git, and GitHub to provide a professional development experience.

### Key Benefits

- **Zero-Configuration Setup**: Automated project creation with all necessary dependencies
- **Secure Credential Management**: Leverages Replit Secrets for secure GitHub PAT storage
- **Standardized Workflow**: Consistent development patterns across all projects
- **Time Efficiency**: Reduces setup time from hours to minutes
- **Error Prevention**: Built-in validation and error handling
- **Professional Git Practices**: Automated branch management and commit workflows

---

## 🚀 Features

### Project Automation
- **Automated Clarinet Integration**: Seamless project scaffolding with `clarinet new`
- **Git Repository Setup**: Complete Git initialization, remote configuration, and initial commit
- **GitHub Integration**: Automatic repository creation and secure authentication
- **Branch Management**: Automated feature branch creation and checkout
- **Contract Generation**: Instant smart contract template creation
- **IDE Integration**: Automatic file opening in Replit editor

### Development Workflow
- **Code Validation**: Integrated `clarinet check` execution
- **Intelligent Commit Management**: Both custom and standardized commit workflows
- **Security Best Practices**: Automatic script exclusion from version control
- **Error Handling**: Comprehensive validation and user-friendly error messages

### Security & Privacy
- **Token Security**: GitHub PAT stored securely via Replit Secrets
- **Clean Repositories**: Utility scripts automatically excluded from Git tracking
- **Validation Guards**: Multiple layers of input validation and error checking

---

## 📋 Prerequisites

### Required Tools
- **Clarinet CLI**: Clarity development toolkit (v0.31.1 or compatible)
- **Git**: Version control system (pre-installed in Replit)
- **Bash Shell**: Unix shell environment (available in Replit Linux environment)

### Required Configuration
1. **GitHub Personal Access Token (PAT)**:
   - Create a PAT with repository permissions at [GitHub Settings](https://github.com/settings/tokens)
   - Store as Replit Secret with key `GITHUB_PAT`
   - Navigate to **Secrets** tab (🔒 lock icon) in Replit sidebar

2. **GitHub Account**: Active GitHub account for repository hosting

### Replit Environment Setup
```bash
# Verify Clarinet installation
clarinet --version

# Verify Git configuration
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## 📖 Usage Guide

### Initial Project Setup

The `full_clarity_setup.sh` script handles complete project initialization. It requires three parameters and performs all setup tasks automatically.

**Syntax:**
```bash
./full_clarity_setup.sh <project_name> <branch_name> <contract_name>
```

**Parameters:**
- `project_name`: The name of your new Clarity project (alphanumeric, hyphens allowed)
- `branch_name`: Initial feature branch name (e.g., `feature-new-contract`, `dev-initial`)
- `contract_name`: Name of the first smart contract to create

**Example:**
```bash
./full_clarity_setup.sh stx-defi-protocol feature-staking-rewards staking-contract
```

**What This Creates:**
```
stx-defi-protocol/
├── contracts/
│   └── staking-contract.clar          # Your smart contract
├── tests/
│   └── staking-contract_test.ts       # Test file
├── settings/
│   ├── Devnet.toml                    # Development network config
│   ├── Testnet.toml                   # Testnet configuration
│   └── Mainnet.toml                   # Mainnet configuration
├── .vscode/                           # VS Code settings
├── Clarinet.toml                      # Project configuration
├── README.md                          # Project documentation
├── .gitignore                         # Git ignore rules
├── ClarCommit.sh                      # Development utility script
└── FinCommit.sh                       # Quick commit utility script
```

### Development Workflow Scripts

Once your project is initialized, navigate to the project directory to use the development utilities:

```bash
cd your-project-name
```

#### Code Validation & Custom Commits

Use `ClarCommit.sh` for thorough development workflows:

```bash
./ClarCommit.sh
```

**This script performs:**
1. Runs `clarinet check` to validate your Clarity code
2. Stages all changes with `git add .`
3. Opens an interactive commit editor for detailed commit messages

**Best Practices for Commit Messages:**
```
feat: implement staking reward calculation logic

- Add stake-tokens function with time-lock mechanism
- Implement reward distribution based on stake duration
- Add comprehensive input validation
- Update contract documentation

Resolves: #123
```

#### Quick Standardized Commits

Use `FinCommit.sh` for rapid README updates and documentation changes:

```bash
./FinCommit.sh
```

**This script performs:**
1. Stages all changes
2. Commits with standardized message: "README.md file updated"
3. Pushes changes to current branch

---

## 🛠 Scripts Reference

### `full_clarity_setup.sh`

**Purpose**: Complete project initialization and setup automation

**Process Flow:**
1. **Validation**: Checks for required arguments and environment variables
2. **Project Creation**: Executes `clarinet new` with automated prompt handling
3. **Documentation**: Creates initial README.md with project name
4. **Version Control**: Initializes Git repository
5. **Utility Setup**: Copies development scripts and configures `.gitignore`
6. **Initial Commit**: Stages and commits initial project structure
7. **Remote Setup**: Configures GitHub remote repository with secure authentication
8. **Branch Creation**: Creates and switches to development branch
9. **Contract Creation**: Generates initial smart contract template
10. **IDE Integration**: Opens contract file in Replit editor

**Error Handling:**
- Validates GitHub PAT availability
- Checks argument count and format
- Verifies successful directory creation
- Provides detailed error messages with resolution steps

**Security Features:**
- Uses Replit Secrets for GitHub PAT storage
- Excludes utility scripts from Git tracking
- Implements secure HTTPS authentication for Git operations

### `ClarCommit.sh`

**Purpose**: Development workflow automation with code validation

**Features:**
- **Code Quality**: Runs `clarinet check` before commit
- **Change Management**: Stages all modifications
- **Interactive Commits**: Opens editor for detailed commit messages
- **Progress Feedback**: Clear visual progress indicators

**Use Cases:**
- Feature development commits
- Bug fix implementations
- Contract updates and modifications
- Documentation updates requiring detailed commit messages

### `FinCommit.sh`

**Purpose**: Quick commit and push for standardized updates

**Features:**
- **Rapid Deployment**: Single command for commit and push
- **Standardized Messaging**: Consistent commit message format
- **Immediate Sync**: Automatic push to remote branch

**Use Cases:**
- README.md updates
- Documentation corrections
- Minor configuration changes
- Quick fixes and patches

---

## ⚙️ Configuration

### Environment Variables

The scripts use the following environment configuration:

```bash
# Required - Store in Replit Secrets
GITHUB_PAT="your_github_personal_access_token"

# Configurable in full_clarity_setup.sh
GITHUB_USERNAME="ImmaObong"  # Update with your GitHub username
```

### Customization Options

#### GitHub Username
Update the username in `full_clarity_setup.sh`:
```bash
# Line 6 in full_clarity_setup.sh
GITHUB_USERNAME="YourGitHubUsername"
```

#### Commit Messages
Modify `FinCommit.sh` for different standardized messages:
```bash
# Line 5 in FinCommit.sh
COMMIT_MESSAGE="Documentation updated"  # Customize as needed
```

#### Default Contract Settings
The scripts use Clarinet's default contract template. For custom templates, modify the contract creation step in `full_clarity_setup.sh`.

---

## 🔐 Security Best Practices

### GitHub PAT Management
- **Never hardcode tokens** in scripts or configuration files
- **Use Replit Secrets** for all sensitive credentials
- **Regular rotation** of GitHub PATs (recommended every 90 days)
- **Minimal permissions** - only grant necessary repository access

### Repository Security
- **Script Exclusion**: Utility scripts are automatically added to `.gitignore`
- **Clean History**: Avoid committing sensitive information
- **Branch Protection**: Consider enabling branch protection rules on GitHub

### Development Security
- **Code Validation**: Always run `clarinet check` before commits
- **Test Coverage**: Implement comprehensive test suites
- **Peer Review**: Use GitHub pull requests for collaborative development

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### "GITHUB_PAT environment variable not found"
**Solution**: 
1. Navigate to Replit Secrets tab (🔒 lock icon)
2. Add new secret: Key = `GITHUB_PAT`, Value = your GitHub token
3. Restart the script

#### "Failed to create project directory"
**Solution**:
- Ensure project name contains only alphanumeric characters and hyphens
- Check available disk space
- Verify Clarinet installation: `clarinet --version`

#### "Permission denied" when running scripts
**Solution**:
```bash
chmod +x *.sh  # Make scripts executable
```

#### Git authentication failures
**Solution**:
1. Verify GitHub PAT has correct permissions
2. Check GitHub PAT expiration date
3. Ensure token includes `repo` scope

### Debug Mode

Enable verbose output for troubleshooting:
```bash
bash -x ./full_clarity_setup.sh project_name branch_name contract_name
```

---

## 🧪 Testing Your Setup

### Quick Validation Test
```bash
# Test script execution permissions
ls -la *.sh

# Verify Clarinet functionality
clarinet --help

# Check Git configuration
git config --list

# Validate GitHub PAT (without exposing the token)
[ -n "$GITHUB_PAT" ] && echo "✅ GitHub PAT configured" || echo "❌ GitHub PAT missing"
```

### End-to-End Test
Create a test project to validate the complete workflow:
```bash
./full_clarity_setup.sh test-project test-branch test-contract
```

---

## 🚀 Advanced Usage

### Batch Project Creation
Create multiple projects with a loop:
```bash
#!/bin/bash
projects=("defi-protocol" "nft-marketplace" "dao-governance")
for project in "${projects[@]}"; do
  ./full_clarity_setup.sh "$project" "feature-initial" "main-contract"
done
```

### Integration with CI/CD
The scripts can be integrated into continuous integration workflows:
```yaml
# Example GitHub Actions integration
- name: Setup Clarity Project
  run: |
    ./full_clarity_setup.sh ${{ env.PROJECT_NAME }} ${{ env.BRANCH_NAME }} ${{ env.CONTRACT_NAME }}
```

### Custom Hooks
Add custom functionality by modifying the scripts:
```bash
# Add to full_clarity_setup.sh after contract creation
echo "14. Running custom initialization..."
# Your custom setup commands here
```

---

## 📚 Best Practices

### Development Workflow
1. **Always start with setup script** for new projects
2. **Use ClarCommit.sh** for all code changes
3. **Run tests regularly** with `clarinet test`
4. **Keep commits atomic** - one logical change per commit
5. **Write descriptive commit messages** following conventional commit format

### Project Organization
- **Meaningful names**: Use descriptive project and contract names
- **Branch naming**: Follow conventions like `feature/`, `bugfix/`, `hotfix/`
- **Documentation**: Keep README files updated with project changes
- **Testing**: Maintain comprehensive test coverage

### Collaboration Guidelines
- **Code reviews**: Use GitHub pull requests for team collaboration
- **Issue tracking**: Utilize GitHub Issues for bug reports and feature requests
- **Documentation**: Keep inline code comments and README files current

---

## 🤝 Contributing

### Reporting Issues
- Use GitHub Issues for bug reports
- Include script output and error messages
- Specify Replit environment details
- Provide steps to reproduce the issue

### Feature Requests
- Submit detailed feature proposals via GitHub Issues
- Explain the use case and expected behavior
- Consider backward compatibility

### Code Contributions
1. Fork the repository
2. Create a feature branch
3. Implement changes with appropriate error handling
4. Test thoroughly in Replit environment
5. Submit pull request with detailed description

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for complete terms and conditions.

---

## 🆘 Support

### Documentation Resources
- **Clarity Language**: [Clarity Documentation](https://docs.stacks.co/clarity)
- **Clarinet Tool**: [Clarinet Documentation](https://docs.hiro.so/clarinet)
- **Stacks Blockchain**: [Stacks Documentation](https://docs.stacks.co)

### Getting Help
- **GitHub Issues**: For bug reports and feature requests
- **Stacks Discord**: Community support and discussions
- **Replit Community**: Platform-specific assistance

### Professional Support
For enterprise implementations or custom development requirements, consider engaging with the Stacks ecosystem's professional service providers.

---

## 📊 Changelog

### v2.0.0 (Current)
- **Enhanced Documentation**: Comprehensive README with detailed usage examples
- **Improved Error Handling**: Better validation and user-friendly error messages
- **Security Enhancements**: Secure GitHub PAT management via Replit Secrets
- **Workflow Optimization**: Streamlined script execution and output formatting

### v1.0.0
- **Initial Release**: Basic automation scripts for Clarity project setup
- **Core Functionality**: Project creation, Git integration, and utility scripts
- **Basic Documentation**: Essential usage instructions

---

## 🔮 Roadmap

### Planned Features
- **Multi-Contract Support**: Enhanced support for complex multi-contract projects
- **Testing Integration**: Automated test runner and coverage reporting
- **Deployment Automation**: Streamlined mainnet and testnet deployment workflows
- **Template System**: Pre-configured contract templates for common use cases
- **Performance Monitoring**: Built-in profiling and optimization suggestions

### Future Enhancements
- **Interactive Setup**: Guided setup wizard for new users
- **Plugin Architecture**: Extensible framework for custom workflow additions
- **Integration APIs**: RESTful APIs for external tool integration
- **Advanced Analytics**: Project metrics and development insights

---

*Built with ❤️ for the Stacks and Clarity developer community*
