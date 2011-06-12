from spreadsheets.spreadsheet import ImportField

class SpreadSheetTemplate(object):

    def __init__(self, template_type, name="", description=None, fields=[]):
        
        self.fields = fields
        self.template_type = template_type
        self.name = name
        self.description = description



full_contact_list = SpreadSheetTemplate(
                        "full_contact_list",
                        name="Full Contact List",
                        description="All of the contact information stored in GoodCloud, including personal and work contact information.",
                        fields=[
                            ImportField("First Name",                    "people",       "Person",       "first_name",   ),
                            ImportField("Last Name",                     "people",       "Person",       "last_name",    ),
                            ImportField("Email",                         "people",       "Person",       "email",        ),
                            ImportField("Home Phone",                    "people",       "Person",       "phone_number", ),
                            ImportField("Home Address 1",                "people",       "Person",       "line_1",       ),
                            ImportField("Home Address 2",                "people",       "Person",       "line_2",       ),
                            ImportField("City",                          "people",       "Person",       "city",         ),
                            ImportField("State",                         "people",       "Person",       "state",        ),
                            ImportField("Zip Code",                      "people",       "Person",       "postal_code",  ),
                            ImportField("Title",                         "people",       "Employee",     "role",         ),
                            ImportField("Work Phone",                    "people",       "Employee",     "phone_number", ),
                            ImportField("Work Email",                    "people",       "Employee",     "email",        ),
                            ImportField("Organization Name",             "people",       "Organization", "name",         ),
                            ImportField("Organization Address 1",        "people",       "Organization", "line_1",       ),
                            ImportField("Organization Address 2",        "people",       "Organization", "line_2",       ),
                            ImportField("Organization City",             "people",       "Organization", "city",         ),
                            ImportField("Organization State",            "people",       "Organization", "state",        ),
                            ImportField("Organization Zip",              "people",       "Organization", "zip",          ),
                        ]
                                    
)

mailing_list = SpreadSheetTemplate(
                        "mailing_list",
                        name="Home Mailing List",
                        description="Home addresses, plain and simple. Great for a mail merge",
                        fields=[
                            ImportField("First Name",           "people",       "Person",       "first_name",   ),
                            ImportField("Last Name",            "people",       "Person",       "last_name",    ),
                            ImportField("Address 1",            "people",       "Person",       "line_1",       ),
                            ImportField("Address 2",            "people",       "Person",       "line_2",       ),
                            ImportField("City",                 "people",       "Person",       "city",         ),
                            ImportField("State",                "people",       "Person",       "state",        ),
                            ImportField("Zip Code",             "people",       "Person",       "postal_code",  ),
                        ]
)
email_list = SpreadSheetTemplate(
                        "email_list",
                        name="Email List",
                        description="First name, last name, and email. A quick copy-paste box is below.",
                        fields=[
                            ImportField("First Name",           "people",       "Person",       "first_name",   ),
                            ImportField("Last Name",            "people",       "Person",       "last_name",    ),
                            ImportField("Email",                "people",       "Person",       "email",        ),
                        ]
)

donations = SpreadSheetTemplate(
                        "donations",
                        name="Donation List",
                        description="All donations entered into GoodCloud, with the contact information of the donor.",
                        fields=[
                            ImportField("Date",                 "donations",    "Donation",     "date",         ),
                            ImportField("Amount",               "donations",    "Donation",     "amount",       ),
                            # ImportField("Category",             "donations",    "Donation",     "category",     ),
                            # ImportField("Campaign",             "donations",    "Donation",     "campaign",     ),
                            ImportField("Organization Name",    "people",       "Organization", "name",         ),
                            ImportField("First Name",           "people",       "Person",       "first_name",   ),
                            ImportField("Last Name",            "people",       "Person",       "last_name",    ),
                            ImportField("Email",                "people",       "Person",       "email",        ),
                            ImportField("Home Phone",           "people",       "Person",       "phone_number", ),
                            ImportField("Home Address 1",       "people",       "Person",       "line_1",       ),
                            ImportField("Home Address 2",       "people",       "Person",       "line_2",       ),
                            ImportField("City",                 "people",       "Person",       "city",         ),
                            ImportField("State",                "people",       "Person",       "state",        ),
                            ImportField("Zip Code",             "people",       "Person",       "postal_code",  ),
                        ]
)

donation_summary = SpreadSheetTemplate(
                        "donation_summary",
                        name="Donation Summary List",
                        description="Summary of donations, per person. Includes monthly and yearly totals for all donations in GoodCloud, with the contact information of the donor.",
                        fields=[
                            # ImportField("Date",                 "donations",    "Donation",     "date",         ),
                            # ImportField("Amount",               "donations",    "Donation",     "amount",       ),
                            # ImportField("Category",             "donations",    "Donation",     "category",     ),
                            # ImportField("Campaign",             "donations",    "Donation",     "campaign",     ),
                            
                            ImportField("First Name",           "people",       "Person",       "first_name",   ),
                            ImportField("Last Name",            "people",       "Person",       "last_name",    ),
                            ImportField("Email",                "people",       "Person",       "email",        ),
                            ImportField("Home Phone",           "people",       "Person",       "phone_number", ),
                            ImportField("Home Address 1",       "people",       "Person",       "line_1",       ),
                            ImportField("Home Address 2",       "people",       "Person",       "line_2",       ),
                            ImportField("City",                 "people",       "Person",       "city",         ),
                            ImportField("State",                "people",       "Person",       "state",        ),
                            ImportField("Zip Code",             "people",       "Person",       "postal_code",  ),
                            ImportField("Organization Name",    "people",       "Organization", "name",         ),

                            # ImportField("2011 Total",           "people",       "Person",       "donation_current_year",   ),
                            # ImportField("2011 Jan",           "people",       "Person",       "donation_current_year",   ),
                        ]
)



volunteer_hours = SpreadSheetTemplate(
                        "volunteer_hours",
                        name="Volunteer Shifts",
                        description="All volunteer hours recorded in GoodCloud, with the contact information of the volunteer.",
                        fields=[
                            ImportField("Date",                 "volunteers",    "CompletedShift",     "date",       ),
                            ImportField("Hours",                "volunteers",    "CompletedShift",     "duration",   ),
                            # ImportField("Category",            "event",         "CompletedShift",     "shift",      ),
                           
                            ImportField("First Name",           "people",       "Person",       "first_name",   ),
                            ImportField("Last Name",            "people",       "Person",       "last_name",    ),
                            ImportField("Email",                "people",       "Person",       "email",        ),
                            ImportField("Home Phone",           "people",       "Person",       "phone_number", ),
                            ImportField("Home Address 1",       "people",       "Person",       "line_1",       ),
                            ImportField("Home Address 2",       "people",       "Person",       "line_2",       ),
                            ImportField("City",                 "people",       "Person",       "city",         ),
                            ImportField("State",                "people",       "Person",       "state",        ),
                            ImportField("Zip Code",             "people",       "Person",       "postal_code",  ),
                            ImportField("Organization Name",    "people",       "Organization", "name",         ),
                        ]
)

volunteer_hour_summary = SpreadSheetTemplate(
                        "volunteer_hour_summary",
                        name="Volunteer Hour Summary",
                        description="Total of volunteer hours, per person. Includes monthly and yearly totals for all shifts in GoodCloud, with the contact information of the volunteer.",
                        fields=[
                            ImportField("Date",                 "volunteers",    "CompletedShift",     "date",       ),
                            ImportField("Hours",                "volunteers",    "CompletedShift",     "duration",   ),
                            # ImportField("Category",            "event",         "CompletedShift",     "shift",      ),
                           
                            ImportField("First Name",           "people",       "Person",       "first_name",   ),
                            ImportField("Last Name",            "people",       "Person",       "last_name",    ),
                            ImportField("Email",                "people",       "Person",       "email",        ),
                            ImportField("Home Phone",           "people",       "Person",       "phone_number", ),
                            ImportField("Home Address 1",       "people",       "Person",       "line_1",       ),
                            ImportField("Home Address 2",       "people",       "Person",       "line_2",       ),
                            ImportField("City",                 "people",       "Person",       "city",         ),
                            ImportField("State",                "people",       "Person",       "state",        ),
                            ImportField("Zip Code",             "people",       "Person",       "postal_code",  ),
                            ImportField("Organization Name",    "people",       "Organization", "name",         ),

                            # ImportField("2011 Total",           "people",       "Person",       "donation_current_year",   ),
                            # ImportField("2011 Jan",           "people",       "Person",       "donation_current_year",   ),
                        ]
)



SPREADSHEET_TEMPLATES = [
    full_contact_list,
    mailing_list,
    email_list,
    donations,
    # donation_summary,
    volunteer_hours,
    # volunteer_hour_summary,
]