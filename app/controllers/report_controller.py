#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Report Controller
Handles report generation and data analysis
"""

from typing import Dict, List, Optional
import logging
import os
from datetime import datetime, timedelta

from .base_controller import BaseController

logger = logging.getLogger(__name__)


class ReportController(BaseController):
    """Controller for generating various reports"""

    def __init__(self, property_model, owner_model, view=None):
        super().__init__(None, view)
        self.property_model = property_model
        self.owner_model = owner_model
        self.reports_directory = "reports"
        self._ensure_reports_directory()

    def _ensure_reports_directory(self):
        """Ensure reports directory exists"""
        if not os.path.exists(self.reports_directory):
            os.makedirs(self.reports_directory)

    def generate_property_summary_report(self, filters: Dict = None) -> Optional[str]:
        """Generate comprehensive property summary report"""
        try:
            # Get properties based on filters
            if filters:
                properties = self.property_model.advanced_search(filters)
            else:
                properties = self.property_model.get_all()

            if not properties:
                self.handle_error("No properties found for report")
                return None

            # Generate report content
            report_content = self._create_property_summary_content(properties)

            # Save report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"property_summary_report_{timestamp}.txt"
            filepath = os.path.join(self.reports_directory, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report_content)

            self.handle_success(f"Property summary report generated: {filename}")
            logger.info(f"Property summary report saved: {filepath}")
            return filepath

        except Exception as e:
            self.handle_error(f"Error generating property summary report: {str(e)}")
            return None

    def generate_owner_properties_report(self, owner_code: str = None) -> Optional[str]:
        """Generate report showing owners and their properties"""
        try:
            if owner_code:
                # Get specific owner's properties
                owner = self.owner_model.get_by_id(owner_code)
                if not owner:
                    self.handle_error(f"Owner not found: {owner_code}")
                    return None
                owners_data = [owner]
            else:
                # Get all owners
                owners_data = self.owner_model.get_all()

            if not owners_data:
                self.handle_error("No owners found for report")
                return None

            # Get properties for each owner
            report_data = []
            for owner in owners_data:
                owner_properties = self.property_model.search({
                    'owner_code': owner['Ownercode']
                })
                report_data.append({
                    'owner': owner,
                    'properties': owner_properties
                })

            # Generate report content
            report_content = self._create_owner_properties_content(report_data)

            # Save report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            suffix = f"_{owner_code}" if owner_code else ""
            filename = f"owner_properties_report{suffix}_{timestamp}.txt"
            filepath = os.path.join(self.reports_directory, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report_content)

            self.handle_success(f"Owner properties report generated: {filename}")
            logger.info(f"Owner properties report saved: {filepath}")
            return filepath

        except Exception as e:
            self.handle_error(f"Error generating owner properties report: {str(e)}")
            return None

    def generate_market_analysis_report(self) -> Optional[str]:
        """Generate market analysis report with statistics"""
        try:
            # Get all properties for analysis
            properties = self.property_model.get_all()
            if not properties:
                self.handle_error("No properties found for analysis")
                return None

            # Perform analysis
            analysis_data = self._perform_market_analysis(properties)

            # Generate report content
            report_content = self._create_market_analysis_content(analysis_data)

            # Save report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"market_analysis_report_{timestamp}.txt"
            filepath = os.path.join(self.reports_directory, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report_content)

            self.handle_success(f"Market analysis report generated: {filename}")
            logger.info(f"Market analysis report saved: {filepath}")
            return filepath

        except Exception as e:
            self.handle_error(f"Error generating market analysis report: {str(e)}")
            return None

    def generate_custom_report(self, criteria: Dict, report_type: str = 'detailed') -> Optional[str]:
        """Generate custom report based on specific criteria"""
        try:
            # Get properties based on criteria
            properties = self.property_model.advanced_search(criteria)

            if not properties:
                self.handle_error("No properties match the specified criteria")
                return None

            # Generate report based on type
            if report_type == 'summary':
                report_content = self._create_summary_report(properties, criteria)
            elif report_type == 'detailed':
                report_content = self._create_detailed_report(properties, criteria)
            elif report_type == 'comparison':
                report_content = self._create_comparison_report(properties, criteria)
            else:
                self.handle_error(f"Unknown report type: {report_type}")
                return None

            # Save report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"custom_{report_type}_report_{timestamp}.txt"
            filepath = os.path.join(self.reports_directory, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report_content)

            self.handle_success(f"Custom {report_type} report generated: {filename}")
            logger.info(f"Custom report saved: {filepath}")
            return filepath

        except Exception as e:
            self.handle_error(f"Error generating custom report: {str(e)}")
            return None

    def export_report_to_csv(self, properties: List[Dict], filename: str = None) -> Optional[str]:
        """Export properties data to CSV format"""
        try:
            import csv

            if not properties:
                self.handle_error("No data to export")
                return None

            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"properties_export_{timestamp}.csv"

            filepath = os.path.join(self.reports_directory, filename)

            # Define CSV headers
            headers = [
                'Property Code', 'Company Code', 'Property Type', 'Build Type',
                'Year Built', 'Area (sqm)', 'Facade (m)', 'Depth (m)',
                'Bedrooms', 'Bathrooms', 'Corner Property', 'Offer Type',
                'Province', 'Region', 'Address', 'Owner Name', 'Owner Phone',
                'Description'
            ]

            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)

                for prop in properties:
                    row = [
                        prop.get('realstatecode', ''),
                        prop.get('Companyco', ''),
                        prop.get('property_type_desc', ''),
                        prop.get('build_type_desc', ''),
                        prop.get('Yearmake', ''),
                        prop.get('Property-area', ''),
                        prop.get('Property-facade', ''),
                        prop.get('Property-depth', ''),
                        prop.get('N-of-bedrooms', ''),
                        prop.get('N-of bathrooms', ''),
                        'Yes' if prop.get('Property-corner') else 'No',
                        prop.get('offer_type_desc', ''),
                        prop.get('province_desc', ''),
                        prop.get('region_desc', ''),
                        prop.get('Property-address', ''),
                        prop.get('ownername', ''),
                        prop.get('ownerphone', ''),
                        prop.get('Descriptions', '')
                    ]
                    writer.writerow(row)

            self.handle_success(f"Data exported to CSV: {filename}")
            logger.info(f"CSV export saved: {filepath}")
            return filepath

        except Exception as e:
            self.handle_error(f"Error exporting to CSV: {str(e)}")
            return None

    def _create_property_summary_content(self, properties: List[Dict]) -> str:
        """Create property summary report content"""
        total_properties = len(properties)

        # Calculate statistics
        total_area = sum(float(p.get('Property-area', 0) or 0) for p in properties)
        avg_area = total_area / total_properties if total_properties > 0 else 0

        # Count by property types
        type_counts = {}
        for prop in properties:
            prop_type = prop.get('property_type_desc', 'Unknown')
            type_counts[prop_type] = type_counts.get(prop_type, 0) + 1

        # Count by offer types
        offer_counts = {}
        for prop in properties:
            offer_type = prop.get('offer_type_desc', 'Unknown')
            offer_counts[offer_type] = offer_counts.get(offer_type, 0) + 1

        # Generate report
        report = f"""
PROPERTY SUMMARY REPORT
======================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

OVERVIEW
--------
Total Properties: {total_properties}
Total Area: {total_area:,.2f} sqm
Average Area: {avg_area:.2f} sqm

PROPERTY TYPES
--------------
"""
        for prop_type, count in sorted(type_counts.items()):
            percentage = (count / total_properties) * 100
            report += f"{prop_type}: {count} ({percentage:.1f}%)\n"

        report += "\nOFFER TYPES\n-----------\n"
        for offer_type, count in sorted(offer_counts.items()):
            percentage = (count / total_properties) * 100
            report += f"{offer_type}: {count} ({percentage:.1f}%)\n"

        report += "\nPROPERTY DETAILS\n" + "="*50 + "\n"

        for i, prop in enumerate(properties, 1):
            report += f"\n{i}. {prop.get('realstatecode', 'N/A')}\n"
            report += f"   Type: {prop.get('property_type_desc', 'N/A')}\n"
            report += f"   Area: {prop.get('Property-area', 'N/A')} sqm\n"
            report += f"   Location: {prop.get('Property-address', 'N/A')}\n"
            report += f"   Owner: {prop.get('ownername', 'N/A')}\n"

        return report

    def _create_owner_properties_content(self, report_data: List[Dict]) -> str:
        """Create owner properties report content"""
        total_owners = len(report_data)
        total_properties = sum(len(data['properties']) for data in report_data)

        report = f"""
OWNER PROPERTIES REPORT
======================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

OVERVIEW
--------
Total Owners: {total_owners}
Total Properties: {total_properties}
Average Properties per Owner: {total_properties / total_owners if total_owners > 0 else 0:.1f}

OWNER DETAILS
=============
"""

        for data in report_data:
            owner = data['owner']
            properties = data['properties']

            report += f"\nOwner: {owner.get('ownername', 'N/A')}\n"
            report += f"Code: {owner.get('Ownercode', 'N/A')}\n"
            report += f"Phone: {owner.get('ownerphone', 'N/A')}\n"
            report += f"Properties: {len(properties)}\n"

            if properties:
                report += "Property List:\n"
                for prop in properties:
                    report += f"  - {prop.get('realstatecode', 'N/A')} "
                    report += f"({prop.get('property_type_desc', 'N/A')}) "
                    report += f"{prop.get('Property-area', 'N/A')} sqm\n"
            else:
                report += "No properties found.\n"

            report += "-" * 50 + "\n"

        return report

    def _create_market_analysis_content(self, analysis_data: Dict) -> str:
        """Create market analysis report content"""
        report = f"""
MARKET ANALYSIS REPORT
=====================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

MARKET OVERVIEW
---------------
Total Properties: {analysis_data['total_properties']}
Total Market Area: {analysis_data['total_area']:,.2f} sqm
Average Property Size: {analysis_data['avg_area']:.2f} sqm

PROPERTY TYPE DISTRIBUTION
-------------------------
"""
        for prop_type, stats in analysis_data['type_distribution'].items():
            report += f"{prop_type}:\n"
            report += f"  Count: {stats['count']}\n"
            report += f"  Percentage: {stats['percentage']:.1f}%\n"
            report += f"  Total Area: {stats['total_area']:,.2f} sqm\n"
            report += f"  Avg Area: {stats['avg_area']:.2f} sqm\n\n"

        report += "REGIONAL DISTRIBUTION\n" + "-" * 20 + "\n"
        for region, stats in analysis_data['regional_distribution'].items():
            report += f"{region}: {stats['count']} properties ({stats['percentage']:.1f}%)\n"

        report += f"\nMARKET TRENDS\n" + "-" * 13 + "\n"
        report += f"Properties Built in Last 5 Years: {analysis_data['recent_properties']}\n"
        report += f"Corner Properties: {analysis_data['corner_properties']}\n"
        report += f"Average Bedrooms: {analysis_data['avg_bedrooms']:.1f}\n"
        report += f"Average Bathrooms: {analysis_data['avg_bathrooms']:.1f}\n"

        return report

    def _create_detailed_report(self, properties: List[Dict], criteria: Dict) -> str:
        """Create detailed custom report"""
        report = f"""
DETAILED PROPERTY REPORT
=======================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Filter Criteria: {criteria}

PROPERTIES FOUND: {len(properties)}
"""

        for prop in properties:
            report += f"\n" + "="*60 + "\n"
            report += f"Property Code: {prop.get('realstatecode', 'N/A')}\n"
            report += f"Company Code: {prop.get('Companyco', 'N/A')}\n"
            report += f"Type: {prop.get('property_type_desc', 'N/A')}\n"
            report += f"Build Type: {prop.get('build_type_desc', 'N/A')}\n"
            report += f"Year: {prop.get('Yearmake', 'N/A')}\n"
            report += f"Area: {prop.get('Property-area', 'N/A')} sqm\n"
            report += f"Facade: {prop.get('Property-facade', 'N/A')} m\n"
            report += f"Depth: {prop.get('Property-depth', 'N/A')} m\n"
            report += f"Bedrooms: {prop.get('N-of-bedrooms', 'N/A')}\n"
            report += f"Bathrooms: {prop.get('N-of bathrooms', 'N/A')}\n"
            report += f"Corner: {'Yes' if prop.get('Property-corner') else 'No'}\n"
            report += f"Offer Type: {prop.get('offer_type_desc', 'N/A')}\n"
            report += f"Province: {prop.get('province_desc', 'N/A')}\n"
            report += f"Region: {prop.get('region_desc', 'N/A')}\n"
            report += f"Address: {prop.get('Property-address', 'N/A')}\n"
            report += f"Owner: {prop.get('ownername', 'N/A')}\n"
            report += f"Phone: {prop.get('ownerphone', 'N/A')}\n"
            report += f"Description: {prop.get('Descriptions', 'N/A')}\n"

        return report

    def _perform_market_analysis(self, properties: List[Dict]) -> Dict:
        """Perform market analysis on properties data"""
        total_properties = len(properties)
        total_area = sum(float(p.get('Property-area', 0) or 0) for p in properties)
        avg_area = total_area / total_properties if total_properties > 0 else 0

        # Type distribution
        type_distribution = {}
        for prop in properties:
            prop_type = prop.get('property_type_desc', 'Unknown')
            if prop_type not in type_distribution:
                type_distribution[prop_type] = {
                    'count': 0,
                    'total_area': 0
                }
            type_distribution[prop_type]['count'] += 1
            type_distribution[prop_type]['total_area'] += float(prop.get('Property-area', 0) or 0)

        # Calculate percentages and averages
        for prop_type, stats in type_distribution.items():
            stats['percentage'] = (stats['count'] / total_properties) * 100
            stats['avg_area'] = stats['total_area'] / stats['count'] if stats['count'] > 0 else 0

        # Regional distribution
        regional_distribution = {}
        for prop in properties:
            region = prop.get('region_desc', 'Unknown')
            if region not in regional_distribution:
                regional_distribution[region] = {'count': 0}
            regional_distribution[region]['count'] += 1

        for region, stats in regional_distribution.items():
            stats['percentage'] = (stats['count'] / total_properties) * 100

        # Additional statistics
        current_year = datetime.now().year
        recent_properties = sum(1 for p in properties
                              if p.get('Yearmake') and int(p.get('Yearmake', 0)) >= current_year - 5)

        corner_properties = sum(1 for p in properties if p.get('Property-corner'))

        bedrooms = [int(p.get('N-of-bedrooms', 0) or 0) for p in properties]
        bathrooms = [int(p.get('N-of bathrooms', 0) or 0) for p in properties]

        avg_bedrooms = sum(bedrooms) / len(bedrooms) if bedrooms else 0
        avg_bathrooms = sum(bathrooms) / len(bathrooms) if bathrooms else 0

        return {
            'total_properties': total_properties,
            'total_area': total_area,
            'avg_area': avg_area,
            'type_distribution': type_distribution,
            'regional_distribution': regional_distribution,
            'recent_properties': recent_properties,
            'corner_properties': corner_properties,
            'avg_bedrooms': avg_bedrooms,
            'avg_bathrooms': avg_bathrooms
        }

    def _create_summary_report(self, properties: List[Dict], criteria: Dict) -> str:
        """Create summary custom report"""
        return f"""
SUMMARY REPORT
==============
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Filter Criteria: {criteria}

Total Properties Found: {len(properties)}
Total Area: {sum(float(p.get('Property-area', 0) or 0) for p in properties):,.2f} sqm
Average Area: {sum(float(p.get('Property-area', 0) or 0) for p in properties) / len(properties) if properties else 0:.2f} sqm

Property Codes:
{chr(10).join(f"- {p.get('realstatecode', 'N/A')}" for p in properties)}
"""

    def _create_comparison_report(self, properties: List[Dict], criteria: Dict) -> str:
        """Create comparison custom report"""
        if len(properties) < 2:
            return "Comparison report requires at least 2 properties."

        report = f"""
PROPERTY COMPARISON REPORT
=========================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Filter Criteria: {criteria}

Comparing {len(properties)} Properties:

"""

        # Create comparison table
        headers = ['Property Code', 'Type', 'Area', 'Bedrooms', 'Bathrooms', 'Year', 'Owner']
        report += f"{'Property Code':<15} {'Type':<15} {'Area':<10} {'Bed':<5} {'Bath':<5} {'Year':<6} {'Owner':<20}\n"
        report += "-" * 80 + "\n"

        for prop in properties:
            report += f"{prop.get('realstatecode', 'N/A'):<15} "
            report += f"{prop.get('property_type_desc', 'N/A')[:14]:<15} "
            report += f"{prop.get('Property-area', 'N/A'):<10} "
            report += f"{prop.get('N-of-bedrooms', 'N/A'):<5} "
            report += f"{prop.get('N-of bathrooms', 'N/A'):<5} "
            report += f"{prop.get('Yearmake', 'N/A'):<6} "
            report += f"{prop.get('ownername', 'N/A')[:19]:<20}\n"

        return report
