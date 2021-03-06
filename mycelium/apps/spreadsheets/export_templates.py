import datetime
from collections import OrderedDict

from accounts.managers import get_or_404_by_account
from spreadsheets.spreadsheet import ImportField, SpreadsheetRow
from people.models import Person
from organizations.models import Organization
from volunteers.models import CompletedShift
from donors.models import Donation
from conversations.models import Conversation





class TargetObjectBasedTemplate(object):

    def get_primary_target(self, account=None, target_id=None, force_refresh=False):
        if not hasattr(self,"primary_target") or force_refresh:
            self.primary_target = get_or_404_by_account(self.model, account, target_id)
        
        return self.primary_target



class PersonBasedTemplate(TargetObjectBasedTemplate):
    model = Person
    row_descriptor = "people"


    def get_target_object_people_Person(self):
        return self.get_primary_target(), False           

    def get_target_object_people_Employee(self):
        return self.get_target_object_people_Person()[0].primary_job, False

    def get_target_object_people_Organization(self):
        if self.get_target_object_people_Employee()[0]:
            return self.get_target_object_people_Employee()[0].organization, False
        else: 
            return None, False

class DonationBasedTemplate(TargetObjectBasedTemplate):
    model = Donation
    person_field = "donor.person"
    row_descriptor = "donations"

    def get_target_object_donors_Donation(self):
        return self.get_primary_target(), False

    def get_target_object_people_Person(self):
        return self.get_target_object_donors_Donation()[0].donor.person, False

    def get_target_object_people_Employee(self):
        return self.get_target_object_people_Person()[0].primary_job, False

    def get_target_object_people_Organization(self):
        if self.get_target_object_people_Employee()[0]:
            return self.get_target_object_people_Employee()[0].organization, False
        else: 
            return None, False


class CompletedShiftBasedTemplate(TargetObjectBasedTemplate):
    model = CompletedShift
    person_field = "volunteer.person"
    row_descriptor = "volunteer shifts"

    def get_target_object_volunteers_CompletedShift(self):
        return self.get_primary_target(), False

    def get_target_object_people_Person(self):
        return self.get_target_object_volunteers_CompletedShift()[0].volunteer.person, False

    def get_target_object_people_Organization(self):
        if self.get_target_object_people_Person()[0].primary_job:
            return self.get_target_object_people_Person()[0].primary_job.organization, False
        else: 
            return None, False


class ConversationBasedTemplate(TargetObjectBasedTemplate):
    model = Conversation
    person_field = "person"
    row_descriptor = "conversations"

    def get_target_object_conversations_Conversation(self):
        return self.get_primary_target(), False

    def get_target_object_people_Person(self):
        return self.get_target_object_conversations_Conversation()[0].person, False


    def get_target_object_accounts_UserAccount(self):
        return self.get_target_object_conversations_Conversation()[0].staff, False


class OrganizationBasedTemplate(TargetObjectBasedTemplate):
    model = Organization
    row_descriptor = "organizations"

    def get_target_object_organizations_Organization(self):
        return self.get_primary_target(), False




class FullContactListTemplate(PersonBasedTemplate):
    template_type = "full_contact_list"
    name = "Full Contact List"
    description = "All of the contact information stored in GoodCloud, including personal and work contact information."
    fields = OrderedDict([
        ("first_name",          ImportField("First Name",                    "people",       "Person",       "first_name",      )),
        ("last_name",           ImportField("Last Name",                     "people",       "Person",       "last_name",       )),
        ("email",               ImportField("Email",                         "people",       "Person",       "email",           )),
        ("phone_number",        ImportField("Home Phone",                    "people",       "Person",       "phone_number",    )),
        ("line_1",              ImportField("Home Address 1",                "people",       "Person",       "line_1",          )),
        ("line_2",              ImportField("Home Address 2",                "people",       "Person",       "line_2",          )),
        ("city",                ImportField("City",                          "people",       "Person",       "city",            )),
        ("state",               ImportField("State",                         "people",       "Person",       "state",           )),
        ("postal_code",         ImportField("Zip Code",                      "people",       "Person",       "postal_code",     )),
        ("org_role",            ImportField("Title",                         "people",       "Employee",     "role",            )),
        ("org_phone_number",    ImportField("Work Phone",                    "people",       "Employee",     "phone_number",    )),
        ("org_email",           ImportField("Work Email",                    "people",       "Employee",     "email",           )),
        ("org_name",            ImportField("Organization Name",             "people",       "Organization", "name",            )),
        ("org_line_1",          ImportField("Organization Address 1",        "people",       "Organization", "line_1",          )),
        ("org_line_2",          ImportField("Organization Address 2",        "people",       "Organization", "line_2",          )),
        ("org_city",            ImportField("Organization City",             "people",       "Organization", "city",            )),
        ("org_state",           ImportField("Organization State",            "people",       "Organization", "state",           )),
        ("org_postal_code",     ImportField("Organization Zip",              "people",       "Organization", "postal_code",     )),
        ("birth_month",         ImportField("Birth Month",                   "people",       "Person",       "birth_month",     )),
        ("birth_date",          ImportField("Birth Day",                     "people",       "Person",       "birth_day",       )),
        ("birth_year",          ImportField("Birth Year",                    "people",       "Person",       "birth_year",      )),
        ("birthday",            ImportField("Birthday",                      "people",       "Person",       "actual_birthday", )),
        ("goodcloud_id",        ImportField("GoodCloud ID",                  "people",       "Person",       "id",           )),
    ])

class FullContactListTemplateInstance(FullContactListTemplate,SpreadsheetRow):
    pass
                                    
class MailingListTemplate (PersonBasedTemplate):
    template_type = "mailing_list"
    name = "Home Mailing List"
    description = "Home addresses, plain and simple. Great for mail merges."
    fields = OrderedDict([
        ("first_name",          ImportField("First Name",           "people",       "Person",       "first_name",   )),
        ("last_name",           ImportField("Last Name",            "people",       "Person",       "last_name",    )),
        ("line_1",              ImportField("Address 1",            "people",       "Person",       "line_1",       )),
        ("line_2",              ImportField("Address 2",            "people",       "Person",       "line_2",       )),
        ("city",                ImportField("City",                 "people",       "Person",       "city",         )),
        ("state",               ImportField("State",                "people",       "Person",       "state",        )),
        ("postal_code",         ImportField("Zip Code",             "people",       "Person",       "postal_code",  )),
        ("goodcloud_id",        ImportField("GoodCloud ID",         "people",       "Person",       "id",           )),
    ])

class MailingListTemplateInstance(MailingListTemplate,SpreadsheetRow):
    pass

class EmailListTemplate (PersonBasedTemplate):
    template_type = "email_list"
    name = "Email List"
    description = "First name, last name, and email. A quick copy-paste box is below."
    fields = OrderedDict([
        ("first_name",          ImportField("First Name",           "people",       "Person",       "first_name",   )),
        ("last_name",           ImportField("Last Name",            "people",       "Person",       "last_name",    )),
        ("email",               ImportField("Email",                "people",       "Person",       "primary_email",)),
    ])

class EmailListTemplateInstance(EmailListTemplate,SpreadsheetRow):
    pass

        
class ConversationsTemplate (ConversationBasedTemplate):
    template_type = "conversations"
    name = "Conversations"
    description = "All conversations, including when they were, who they were with, and the full transcript."
    fields = OrderedDict([
        ("date",                ImportField("Date",                 "conversations",    "Conversation",     "date",                 )),
        ("staff",               ImportField("Staff Member",         "accounts",         "UserAccount",      "full_name",            )),
        ("converation_type",    ImportField("Conversation Type",    "conversations",    "Conversation",     "conversation_type",    )),
        ("first_name",          ImportField("First Name",           "people",           "Person",           "first_name",           )),
        ("last_name",           ImportField("Last Name",            "people",           "Person",           "last_name",            )),
        ("body",                ImportField("Transcript",           "conversations",    "Conversation",     "body",                 )),
        ("goodcloud_id",        ImportField("GoodCloud ID",         "people",           "Person",           "id",                   )),
    ])

class ConversationsTemplateInstance(ConversationsTemplate,SpreadsheetRow):
    pass


class DonationListTemplate (DonationBasedTemplate):
    template_type = "donations"
    name = "Donation List"
    description = "All donations entered into GoodCloud, with the contact information of the donor."
    fields = OrderedDict([
        ("date",                  ImportField("Date",                 "donors",       "Donation",     "date",         )),
        ("amount",                ImportField("Amount",               "donors",       "Donation",     "amount",       )),
        ("type",                  ImportField("Type",                 "donors",       "Donation",     "type",         )),
        ("notes",                 ImportField("Notes",                "donors",       "Donation",     "notes",        )),
        ("in_memory_of",          ImportField("In Memory Of",         "donors",       "Donation",     "memoree_name", )),
        ("in_honor_of",           ImportField("In Honor Of",          "donors",       "Donation",     "honoree_name", )),
        # ("category",              ImportField("Category",             "donors",    "Donation",     "category",      )),
        # ("campaign",              ImportField("Campaign",             "donors",    "Donation",     "campaign",      )),
        ("first_name",            ImportField("First Name",           "people",       "Person",       "first_name",   )),
        ("last_name",             ImportField("Last Name",            "people",       "Person",       "last_name",    )),
        ("email",                 ImportField("Email",                "people",       "Person",       "primary_email",)),
        ("phone_number",          ImportField("Home Phone",           "people",       "Person",       "phone_number", )),
        ("line_1",                ImportField("Home Address 1",       "people",       "Person",       "line_1",       )),
        ("line_2",                ImportField("Home Address 2",       "people",       "Person",       "line_2",       )),
        ("city",                  ImportField("City",                 "people",       "Person",       "city",         )),
        ("state",                 ImportField("State",                "people",       "Person",       "state",        )),
        ("postal_code",           ImportField("Zip Code",             "people",       "Person",       "postal_code",  )),
        ("org_name",              ImportField("Organization Name",    "people",       "Organization", "name",         )),
        ("goodcloud_donation_id", ImportField("GoodCloud Donation ID","donors",       "Donation",     "id",           )),
        ("goodcloud_id",          ImportField("GoodCloud ID",         "people",       "Person",     "id",           )),
    ])

class DonationListTemplateInstance(DonationListTemplate,SpreadsheetRow):
    pass

class DonationSummaryListTemplate (PersonBasedTemplate):
    template_type = "donation_summary"
    name = "Donation Summary"
    description = "Summary of donations, per person, including yearly totals, total all-time, and the contact information of the donor."
    fields = OrderedDict([
        ("goodcloud_id",        ImportField("GoodCloud ID",         "people",       "Person",       "id",           )),
        ("first_name",          ImportField("First Name",           "people",       "Person",       "first_name",   )),
        ("last_name",           ImportField("Last Name",            "people",       "Person",       "last_name",    )),
        ("email",               ImportField("Email",                "people",       "Person",       "primary_email",)),
        ("phone_number",        ImportField("Home Phone",           "people",       "Person",       "phone_number", )),
        ("line_1",              ImportField("Home Address 1",       "people",       "Person",       "line_1",       )),
        ("line_2",              ImportField("Home Address 2",       "people",       "Person",       "line_2",       )),
        ("city",                ImportField("City",                 "people",       "Person",       "city",         )),
        ("state",               ImportField("State",                "people",       "Person",       "state",        )),
        ("postal_code",         ImportField("Zip Code",             "people",       "Person",       "postal_code",  )),
        ("name",                ImportField("Organization Name",    "people",       "Organization", "name",         )),

        # fill these out with post_init_setup
        # ("donation_current_year",            ImportField("2011 Total",           "people",       "Person",       "donation_current_year",   )),
        # ("donation_current_year",            ImportField("2011 Jan",           "people",       "Person",       "donation_current_year",   )),
    ])

class DonationSummaryListTemplateInstance(DonationSummaryListTemplate,SpreadsheetRow):
    def __init__(self, *args, **kwargs):
        super(DonationSummaryListTemplateInstance, self).__init__(*args, **kwargs)
        
        self.fields["donations_all_time"] = ImportField("Total Donations all-time",           "people",       "Person",       "donation_totals_all_time")
        if Donation.objects_by_account(self.account).count() > 0:
            oldest = Donation.objects_by_account(self.account).order_by("date")[0].date
            this_year = datetime.date.today().year
            for y in range(oldest.year, this_year+1):
                self.fields["donation_%s" % y] = ImportField("%s Total" % y,           "people",       "Person",       "donation_total_for_year(%s)" % y)


class VolunteerHoursTemplate (CompletedShiftBasedTemplate):
    template_type = "volunteer_hours"
    name = "Volunteer Shifts"
    description = "All volunteer hours recorded in GoodCloud, with the contact information of the volunteer."
    fields = OrderedDict([
        ("date",                ImportField("Date",                 "volunteers",    "CompletedShift",     "date",       )),
        ("duration",            ImportField("Hours",                "volunteers",    "CompletedShift",     "duration",   )),
        # ("shift",               ImportField("Category",            "event",         "CompletedShift",     "shift",      )),
       
        ("first_name",          ImportField("First Name",           "people",       "Person",       "first_name",   )),
        ("last_name",           ImportField("Last Name",            "people",       "Person",       "last_name",    )),
        ("email",               ImportField("Email",                "people",       "Person",       "primary_email",)),
        ("phone_number",        ImportField("Home Phone",           "people",       "Person",       "phone_number", )),
        ("line_1",              ImportField("Home Address 1",       "people",       "Person",       "line_1",       )),
        ("line_2",              ImportField("Home Address 2",       "people",       "Person",       "line_2",       )),
        ("city",                ImportField("City",                 "people",       "Person",       "city",         )),
        ("state",               ImportField("State",                "people",       "Person",       "state",        )),
        ("postal_code",         ImportField("Zip Code",             "people",       "Person",       "postal_code",  )),
        ("name",                ImportField("Organization Name",    "people",       "Organization", "name",         )),
        ("goodcloud_id",        ImportField("GoodCloud ID",         "people",       "Person",     "id",           )),
    ])

class VolunteerHoursTemplateInstance(VolunteerHoursTemplate,SpreadsheetRow):
    pass

class VolunteerHoursSummaryTemplate (PersonBasedTemplate):
    template_type = "volunteer_hour_summary"
    name = "Volunteer Hour Summary"
    description = "Total of volunteer hours, per person, including yearly totals, total all-time, and the contact information of the volunteer."
    fields = OrderedDict([
        
        ("first_name",          ImportField("First Name",           "people",       "Person",       "first_name",   )),
        ("last_name",           ImportField("Last Name",            "people",       "Person",       "last_name",    )),
        ("email",               ImportField("Email",                "people",       "Person",       "primary_email",)),
        ("phone_number",        ImportField("Home Phone",           "people",       "Person",       "phone_number", )),
        ("line_1",              ImportField("Home Address 1",       "people",       "Person",       "line_1",       )),
        ("line_2",              ImportField("Home Address 2",       "people",       "Person",       "line_2",       )),
        ("city",                ImportField("City",                 "people",       "Person",       "city",         )),
        ("state",               ImportField("State",                "people",       "Person",       "state",        )),
        ("postal_code",         ImportField("Zip Code",             "people",       "Person",       "postal_code",  )),
        ("name",                ImportField("Organization Name",    "people",       "Organization", "name",         )),
        ("goodcloud_id",        ImportField("GoodCloud ID",         "people",       "Person",       "id",           )),

        # ("hours_current_year",            ImportField("2011 Total",         "people",       "Person",       "hours_current_year",   )),
        # ("hours_current_year",            ImportField("2011 Jan",           "people",       "Person",       "hours_current_year",   )),
    ])


class VolunteerHoursSummaryTemplateInstance(VolunteerHoursSummaryTemplate,SpreadsheetRow):
    def __init__(self, *args, **kwargs):
        super(VolunteerHoursSummaryTemplateInstance, self).__init__(*args, **kwargs)
        
        self.fields["hours_all_time"] = ImportField("Total Hours all-time",           "people",       "Person",       "volunteer_hours_all_time")
        if CompletedShift.objects_by_account(self.account).count() > 0:
            oldest = CompletedShift.objects_by_account(self.account).order_by("date")[0].date
            this_year = datetime.date.today().year
            for y in range(oldest.year, this_year+1):
                self.fields["hours_%s" % y] = ImportField("%s Total Hours" % y,           "people",       "Person",       "volunteer_hours_for_year(%s)" % y)


class OrganizationsTemplate(OrganizationBasedTemplate):
    template_type = "organizations"
    name = "Organizations"
    description = "All organizations in your GoodCloud, with full contact information."
    fields = OrderedDict([
        ("name",                ImportField("Name",                          "organizations",       "Organization",       "name",                  )),
        ("phone_number",        ImportField("Home Phone",                    "organizations",       "Organization",       "primary_phone_number",  )),
        ("line_1",              ImportField("Home Address 1",                "organizations",       "Organization",       "line_1",                )),
        ("line_2",              ImportField("Home Address 2",                "organizations",       "Organization",       "line_2",                )),
        ("city",                ImportField("City",                          "organizations",       "Organization",       "city",                  )),
        ("state",               ImportField("State",                         "organizations",       "Organization",       "state",                 )),
        ("postal_code",         ImportField("Zip Code",                      "organizations",       "Organization",       "postal_code",           )),
        ("website",             ImportField("Website",                       "organizations",       "Organization",       "website",               )),
        ("twitter_username",    ImportField("Twitter",                       "organizations",       "Organization",       "twitter_username",      )),
        ("goodcloud_id",        ImportField("GoodCloud ID",                  "organizations",       "Organization",       "id",                    )),
    ])

class OrganizationsTemplateInstance(OrganizationsTemplate,SpreadsheetRow):
    pass
           

class CustomTemplate (object):
    template_type = "custom_template"
    name = "Custom Template"
    description = "Pick your own columns and ordering."
    fields =  [ ]


class CustomTemplateInstance(CustomTemplate,SpreadsheetRow):
    pass




SPREADSHEET_TEMPLATES = [
    FullContactListTemplate(),
    MailingListTemplate(),
    EmailListTemplate(),
    ConversationsTemplate(),
    DonationListTemplate(),
    DonationSummaryListTemplate(),
    VolunteerHoursTemplate(),
    VolunteerHoursSummaryTemplate(),
    OrganizationsTemplate(),

    # CustomTemplate(),
]
SPREADSHEET_TEMPLATE_INSTANCES = {
    "full_contact_list"      : FullContactListTemplateInstance,
    "mailing_list"           : MailingListTemplateInstance,
    "email_list"             : EmailListTemplateInstance,
    "conversations"          : ConversationsTemplateInstance,
    "donations"              : DonationListTemplateInstance,
    "donation_summary"       : DonationSummaryListTemplateInstance,   # see post_init_setup
    "volunteer_hours"        : VolunteerHoursTemplateInstance,
    "volunteer_hour_summary" : VolunteerHoursSummaryTemplateInstance,
    "organizations"          : OrganizationsTemplateInstance,
    
    # "custom_template"        : CustomTemplateInstance,
}