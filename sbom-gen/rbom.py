#!/usr/bin/env python3
"""
RBOM Generates SBOM if not present, then processes through VEX analysis
"""

import json
import subprocess
import csv
import sys
import os
from datetime import datetime
import math
global component_count
component_count = 0  # on Ubuntu 22 after SBOM generation  component_count  is about  272525  

def generate_sbom(target="/"):
    """Module 1: Generate SBOM using Syft"""
    global component_count
    print("SBOM Gen...")
    # print("───────────────────────────────────────────────────────────────────────")
    print(f"  Target: {target}")
    
    # Check if Syft is installed
    try:
        result = subprocess.run(["syft", "version"], capture_output=True, check=True)
        # print(f"  Syft version: {result.stdout.decode().strip().split()[1]}")
    except:
        print(" Syft not installed. Install with:")
        print("   curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin")
        return False
    
    # Prepare target
    if not target.startswith("dir:"):
        target = f"dir:{target}"
    
    print("Generating SBOM of target...")
    # print(f"  Running: syft {target} -o cyclonedx-json")
    print("  (This may take 5-10 minutes...)")
    
    # Run Syft
    cmd = ["syft", target, "-o", "cyclonedx-json", "-q"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Write SBOM to file
        with open("sbom.json", "w") as f:
            f.write(result.stdout)
        
        # Parse to count components
        sbom_data = json.loads(result.stdout)
        component_count = len(sbom_data.get('components', []))
        
        print(f"  SBOM generated: sbom.json")
        print(f"  Components found: {component_count}")
        print()
        return True
        
    except subprocess.CalledProcessError as e:
        print(f" Syft scan failed: {e.stderr}")
        return False
    except Exception as e:
        print(f" Error: {e}")
        return False

def run_grype_scan(sbom_file, output_file):
    """Run Grype scan on SBOM and generate CSV report"""
    global component_count
    print("  [*] Running vulnerability scan...")
    print(f"        SBOM: {sbom_file}")
    
    # Check if Grype is installed
    try:
        subprocess.run(["grype", "version"], capture_output=True, check=True)
    except:
        print(" Grype not installed. Install with:")
        print("   curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin")
        return False
    
    # List Existing SBOM Components
    with open('sbom.json') as f:
        sbom = json.load(f)

    count = len(sbom.get('components', []))
    component_count = count
    print(f"        Components: {count}")

    
    # Run Grype
    print()
    print("  Scanning...")
    print("     (This may take 5-10 minutes...)")
    cmd = ["grype", f"sbom:{sbom_file}", "-o", "json", "-q"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        grype_data = json.loads(result.stdout)
        
        # Write intermediate JSON
        with open("grype-report.json", "w") as f:
            json.dump(grype_data, f, indent=2)
        
        # Convert to CSV
        convert_grype_to_csv(grype_data, output_file)
        print(f"    Vulnerability scan complete: {output_file}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f" Grype scan failed: {e.stderr}")
        return False
    except Exception as e:
        print(f" Error: {e}")
        return False

def convert_grype_to_csv(grype_data, csv_file):
    """Convert Grype JSON to CSV format"""
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Installed', 'Fixed-In', 'Type', 'Vulnerability', 'Severity', 'URL'])
        
        if 'matches' in grype_data:
            for match in grype_data['matches']:
                artifact = match.get('artifact', {})
                vuln = match.get('vulnerability', {})
                
                name = artifact.get('name', '')
                version = artifact.get('version', '')
                pkg_type = artifact.get('type', '')
                vuln_id = vuln.get('id', '')
                severity = vuln.get('severity', 'Unknown')
                
                # Get fixed version
                fixed_in = ''
                if 'fix' in vuln and 'versions' in vuln['fix']:
                    fixed_in = ', '.join(vuln['fix']['versions'])
                
                # Get URL
                url = ''
                if 'dataSource' in vuln:
                    url = vuln['dataSource']
                
                writer.writerow([name, version, fixed_in, pkg_type, vuln_id, severity, url])
    
    print(f"    Vulnerability report conversion JSON to CSV format: {csv_file}")

def process_vex(grype_csv, vex_csv):
    """Process Grype CSV through VEX analysis"""
    print()
    print("[*]  Processing through VEX databases...")
    
    vex_records = []
    
    with open(grype_csv, 'r') as f:
        reader = csv.DictReader(f)
        count = 0
        
        for row in reader:
            count += 1
            # if count % 100 == 0:
            if count % 10000 == 0:
                print(f"    Processed: {count} vulnerabilities")
            
            # Extract fields
            name = row['Name']
            version = row['Installed']
            fixed_in = row['Fixed-In']
            pkg_type = row['Type']
            vuln_id = row['Vulnerability']
            severity = row['Severity']
            url = row['URL']
            
            # VEX Analysis
            vex_status = analyze_vex_status(fixed_in, severity)
            exploitability = analyze_exploitability(severity, pkg_type)
            cvss_score = estimate_cvss(severity)
            data_source = extract_data_source(url)
            description = f"{vuln_id} vulnerability in {name} package ({severity} severity)"
            action = generate_action(vex_status, severity, fixed_in)
            last_updated = datetime.now().isoformat()
            
            vex_records.append({
                'Vulnerability': vuln_id,
                'Package': name,
                'Version': version,
                'Severity': severity,
                'CVSS Score': cvss_score,
                'Fixed Version': fixed_in,
                'VEX Status': vex_status,
                'Exploitability': exploitability,
                'Data Source': data_source,
                'Description': description,
                'URLs': url,
                'Action Required': action,
                'Last Updated': last_updated
            })
    
    # Write VEX CSV
    with open(vex_csv, 'w', newline='') as f:
        fieldnames = ['Vulnerability', 'Package', 'Version', 'Severity', 'CVSS Score', 
                     'Fixed Version', 'VEX Status', 'Exploitability', 'Data Source', 
                     'Description', 'URLs', 'Action Required', 'Last Updated']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(vex_records)
    
    print()
    print(f"  VEX analysis complete: {count} vulnerabilities processed")
    print(f"  VEX report: {vex_csv}")
    return True

def analyze_vex_status(fixed_in, severity):
    """Analyze VEX status"""
    if fixed_in and fixed_in not in ['', 'N/A', 'none']:
        return 'fixed'
    if severity.upper() in ['CRITICAL', 'HIGH']:
        return 'under_investigation'
    return 'affected'

def analyze_exploitability(severity, pkg_type):
    """Analyze exploitability"""
    sev = severity.upper()
    if 'lib' in pkg_type.lower():
        if sev == 'CRITICAL':
            return 'High'
        if sev == 'HIGH':
            return 'Medium'
        return 'Low'
    
    if sev == 'CRITICAL':
        return 'High'
    if sev == 'HIGH':
        return 'Medium'
    if sev == 'MEDIUM':
        return 'Low'
    return 'Low'

def estimate_cvss(severity):
    """Estimate CVSS score from severity"""
    mapping = {
        'CRITICAL': 9.5,
        'HIGH': 7.5,
        'MEDIUM': 5.5,
        'LOW': 3.0,
        'NEGLIGIBLE': 0.5,
        'UNKNOWN': 0.0
    }
    return mapping.get(severity.upper(), 0.0)

def extract_data_source(url):
    """Extract data source from URL"""
    if 'nvd.nist.gov' in url:
        return 'NVD'
    if 'github.com' in url:
        return 'GitHub Security Advisory'
    if 'ubuntu.com' in url:
        return 'Ubuntu Security'
    if 'debian.org' in url:
        return 'Debian Security'
    return 'Grype Database'

def generate_action(vex_status, severity, fixed_in):
    """Generate action recommendation"""
    if vex_status == 'fixed':
        if fixed_in:
            return f"Update to version {fixed_in}"
        return "Apply available patch"
    if vex_status == 'under_investigation':
        return "Monitor for updates; apply workarounds if available"
    if severity.upper() in ['CRITICAL', 'HIGH']:
        return "Urgent: Review and mitigate; monitor for patches"
    return "Review and assess impact; monitor for patches"

def calculate_security_score(vex_csv):
	
    """Calculate security score from VEX report"""
    global component_count
    print(" Calculating security score...")
    
    # Count by severity and VEX status
    counts = {
        'critical': 0, 'high': 0, 'medium': 0, 'low': 0, 'negligible': 0, 'unknown': 0,
        'fixed': 0, 'affected': 0, 'under_investigation': 0
    }
    total_vulns = 0
    total_cvss = 0.0
    
    with open(vex_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_vulns += 1
            severity = row['Severity'].lower()
            vex_status = row['VEX Status'].lower()
            cvss = float(row['CVSS Score'])
            total_cvss += cvss
            
            if severity in counts:
                counts[severity] += 1
            else:
                counts['unknown'] += 1
            
            if vex_status in counts:
                counts[vex_status] += 1
    
    # Calculate weighted risk
    weights = {'critical': 10.0, 'high': 7.5, 'medium': 4.0, 'low': 1.0, 'negligible': 0.1, 'unknown': 2.5}
    vex_multipliers = {'fixed': 0.1, 'under_investigation': 0.7, 'affected': 1.0}
    
    base_risk = sum(counts[sev] * weights[sev] for sev in ['critical', 'high', 'medium', 'low', 'negligible', 'unknown'])
    
    if total_vulns > 0:
        risk_per_vuln = base_risk / total_vulns
        weighted_risk = sum(risk_per_vuln * counts[status] * vex_multipliers[status] 
                          for status in ['fixed', 'affected', 'under_investigation'])
        avg_cvss = total_cvss / total_vulns
    else:
        weighted_risk = 0
        avg_cvss = 0
    
    # Calculate score (0-100)
    # Using exponential decay formula for realistic scoring
    # Formula: Score = 100 * exp(-weighted_risk / scale_factor)
    # scale_factor = 300 provides good distribution:
    # - Risk 0-50 → Score: 85-100 (Grade A)
    # - Risk 50-150 → Score: 61-85 (Grade B-D)
    # - Risk 150-400 → Score: 26-61 (Grade D-F)
    # - Risk >400 → Score: 0-26 (Grade F)
    
    if weighted_risk == 0:
        score = 100
    else:
        scale_factor = 300.0  # Adjusted for better sensitivity
        score = int(100 * math.exp(-weighted_risk / scale_factor))
        score = max(0, min(100, score))  # Ensure 0-100 range
    
    # Determine grade and risk level
    if score >= 90:
        grade, risk_level = 'A', 'MINIMAL'
    elif score >= 80:
        grade, risk_level = 'B', 'LOW'
    elif score >= 70:
        grade, risk_level = 'C', 'MEDIUM'
    elif score >= 60:
        grade, risk_level = 'D', 'HIGH'
    elif score >= 50:
        grade, risk_level = 'E', 'HIGH'
    else:
        grade, risk_level = 'F', 'CRITICAL'
    
    # Create report
    report = {
        'overall_score': score,
        'grade': grade,
        'risk_level': risk_level,
        'sbom components found': component_count,
        'total_vulnerabilities': total_vulns,
        'critical_count': counts['critical'],
        'high_count': counts['high'],
        'medium_count': counts['medium'],
        'low_count': counts['low'],
        'negligible_count': counts['negligible'],
        'unknown_count': counts['unknown'],
        'fixed_count': counts['fixed'],
        'affected_count': counts['affected'],
        'under_investigation_count': counts['under_investigation'],
        'average_cvss': round(avg_cvss, 2),
        'weighted_risk': round(weighted_risk, 2),
        'timestamp': datetime.now().isoformat(),
        'report_file': vex_csv
    }
    
    # Write JSON
    with open('security-score.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Write text report
    text_report = f"""╔═══════════════════════════════════════════════════════════════════════╗
║                     RBOM SECURITY SCORE REPORT                        ║
╚═══════════════════════════════════════════════════════════════════════╝

[*] OVERALL SECURITY SCORE: {score}/100
[*] SECURITY GRADE: {grade}
[*] RISK LEVEL: {risk_level}

[*] SBOM components found: {component_count}
[*] Total Vulnerabilities: {total_vulns}
  🔴 Critical: {counts['critical']}
  🟠 High: {counts['high']}
  🟡 Medium: {counts['medium']}
  🟢 Low: {counts['low']}
  ⚪ Negligible: {counts['negligible']}
  ❓ Unknown: {counts['unknown']}

[*] VEX Status Analysis:
  ✅ Fixed: {counts['fixed']} ({counts['fixed']/total_vulns*100:.1f}%)
  ⚠️  Affected: {counts['affected']} ({counts['affected']/total_vulns*100:.1f}%)
  🔍 Under Investigation: {counts['under_investigation']} ({counts['under_investigation']/total_vulns*100:.1f}%)

[*]  Average CVSS Score: {avg_cvss:.2f}/10.0
[*]  Weighted Risk Score: {weighted_risk:.2f}
[*] Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Report Files:
  - VEX Report: {vex_csv}
  - JSON Score: security-score.json
  - Text Report: security-score.txt

═══════════════════════════════════════════════════════════════════════
"""
    
    with open('security-score.txt', 'w') as f:
        f.write(text_report)
    # print(f"\n  [*] SBOM components found: {component_count}")
    # print(f"\n  [*] Security Score: {score}/100 (Grade {grade})")
    print(f"  [*] Risk Level: {risk_level}")
    print(f"  [*] Vulnerabilities: Critical={counts['critical']}, High={counts['high']}, Medium={counts['medium']}, Low={counts['low']}")
    print(f"  [*] VEX Status: Fixed={counts['fixed']}, Affected={counts['affected']}, Under Investigation={counts['under_investigation']}\n")
    
    return True

def generate_scion_config(score_file):
    """Generate SCION configuration"""
    global component_count
    print("  [*] Generating SCION network configuration...")
    
    with open(score_file, 'r') as f:
        score_data = json.load(f)
    
    min_score = 70
    config = {
        'security_score': score_data['overall_score'],
        'min_score': min_score,
        'policy_mode': 'balanced',
        'timestamp': datetime.now().isoformat(),
        'enabled': score_data['overall_score'] >= min_score,
        'grade': score_data['grade'],
        'risk_level': score_data['risk_level']
    }
    
    with open('scion-config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    # print(f"  Current Score: {config['security_score']}/100 (Grade {config['grade']})")
    # print(f"  Minimum Required: {min_score}/100")
    
    if config['enabled']:
    	print()
        # print(f"  Score meets requirements")
    else:
        print(f"    WARNING: Score below minimum threshold!")
    
    print(f"    SCION config: scion-config.json\n")
    return True

def main():
    print("╔═══════════════════════════════════════════════════════════════════════╗")
    print("║                                RBOM                                   ║")
    print("║                                                                       ║")
    print("╚═══════════════════════════════════════════════════════════════════════╝")
    print()
    global component_count
    
    # Check for existing SBOM
    sbom_file = 'sbom.json'
    sbom_exists = os.path.exists(sbom_file)
    
    if sbom_exists:
        # SBOM exists - ask user what to do
        print(f" Found existing SBOM: {sbom_file}")
        print("  Options:")
        print("    1. Use existing SBOM (skip Module 1)")
        print("    2. Regenerate SBOM (run Module 1)")
        print()
        
        while True:
            choice = input("  Select option (1 or 2): ").strip()
            if choice in ['1', '2']:
                break
            print("  Invalid choice. Please enter 1 or 2.")
        
        if choice == '2':
            print()
            target = input("  Enter target directory (default: /): ").strip()
            if not target:
                target = "/"
            print()
            
            print("=" * 71)
            print("MODULE 1: SBOM Generation")
            print("=" * 71)
            print()
            
            if not generate_sbom(target):
                sys.exit(1)
        else:
            print(f"  Skipping Module 1 - Using existing SBOM\n")
    else:
        # No SBOM - automatically generate it
        print(" No existing SBOM found - will generate new SBOM")
        print()
        
        target = input("  Enter target directory to scan (default: /): ").strip()
        if not target:
            target = "/"
        print()
        
        print("=" * 71)
        print("MODULE 1: SBOM Generation")
        print("=" * 71)
        print()
        
        if not generate_sbom(target):
            sys.exit(1)
    
    # Module 2: Grype Scan + VEX
    print("=" * 71)
    print("MODULE 2: Vulnerability Scanning + VEX Analysis")
    print("=" * 71)
    print()
    
    grype_csv = 'vuln-report-raw.csv'
    vex_csv = 'vex-report.csv'
    
    if not run_grype_scan(sbom_file, grype_csv):
        sys.exit(1)
    
    if not process_vex(grype_csv, vex_csv):
        sys.exit(1)
    
    # Module 3: Security Score
    print()
    print("=" * 71)
    print("MODULE 3: Security Score Calculation")
    print("=" * 71)
    print()
    
    if not calculate_security_score(vex_csv):
        sys.exit(1)
    
    # Module 4: SCION
    print("=" * 71)
    print("MODULE 4: SCION Network Integration")
    print("=" * 71)
    print()
    
    if not generate_scion_config('security-score.json'):
        sys.exit(1)
    
    # Summary
    print("=" * 71)
    print(" RBOM Completed Successfully!")
    print("=" * 71)
    print()
    print(f"  [*] SBOM components found:          {component_count}")
    print()
    print("  [*] Generated Files:")
    print(f"    SBOM:                         {sbom_file}")
    print(f"    Vulnerability Report (raw):   {grype_csv}")
    print(f"    VEX Report:                   {vex_csv}")
    print(f"    Security Score (JSON):        security-score.json")
    print(f"    Security Score (text):        security-score.txt")
    print(f"    SCION Config:                 scion-config.json")
    print()

if __name__ == '__main__':
    main()
