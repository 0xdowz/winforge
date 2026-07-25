import json
from typing import Dict, Any, List
from winforge.models.system import SystemHealthReport
from winforge.models.benchmark import BenchmarkSuiteResult


def generate_html_report(
    report: SystemHealthReport,
    eval_findings: List[Dict[str, Any]],
    bench_result: BenchmarkSuiteResult
) -> str:
    """Generates standalone HTML report with embedded CSS styling for WinForge."""
    findings_rows = ""
    for f in eval_findings:
        status_badge = '<span class="badge badge-success">APPROVED</span>' if f["allowed"] else '<span class="badge badge-danger">BLOCKED</span>'
        findings_rows += f"""
        <tr>
            <td><strong>{f['tweak_id']}</strong></td>
            <td>{f['name']}</td>
            <td>{f['risk_level']}</td>
            <td>{status_badge}</td>
            <td>{f['reason']}</td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WinForge Diagnostic Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 30px; }}
        .card {{ background-color: #1e293b; border-radius: 10px; padding: 25px; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }}
        h1 {{ color: #38bdf8; font-size: 28px; margin-top: 0; }}
        h2 {{ color: #f59e0b; font-size: 20px; border-bottom: 2px solid #334155; padding-bottom: 10px; }}
        .score {{ font-size: 48px; font-weight: bold; color: #22c55e; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #334155; }}
        th {{ background-color: #0f172a; color: #38bdf8; }}
        .badge {{ padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }}
        .badge-success {{ background-color: #15803d; color: #ffffff; }}
        .badge-danger {{ background-color: #b91c1c; color: #ffffff; }}
        .footer {{ font-size: 12px; color: #64748b; text-align: center; margin-top: 30px; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>WINFORGE :: SYSTEM DIAGNOSTIC REPORT</h1>
        <p>Generated: {report.timestamp} | OS: {report.os.product_name} ({report.os.architecture}) [Build {report.os.build_number}]</p>
        <div class="score">{round(report.health_score, 1)} / 100</div>
        <p>Overall System Health Scorecard</p>
    </div>

    <div class="card">
        <h2>Hardware Specifications</h2>
        <table>
            <tr><th>Component</th><th>Details</th></tr>
            <tr><td>Processor (CPU)</td><td>{report.cpu.name} ({report.cpu.logical_cores} Cores)</td></tr>
            <tr><td>Memory (RAM)</td><td>{report.ram.total_gb} GB Installed</td></tr>
            <tr><td>Active Power Plan</td><td>{report.power.active_name}</td></tr>
        </table>
    </div>

    <div class="card">
        <h2>Optimization Findings & Recommendations</h2>
        <table>
            <tr>
                <th>Tweak ID</th>
                <th>Optimization Name</th>
                <th>Risk Rating</th>
                <th>Status</th>
                <th>Policy Specification</th>
            </tr>
            {findings_rows}
        </table>
    </div>

    <div class="footer">
        WinForge • Free Open-Source Windows System Diagnostic CLI • Developed by @0xdowz
    </div>
</body>
</html>
"""
    return html
