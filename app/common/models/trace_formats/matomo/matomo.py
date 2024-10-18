from pydantic import BaseModel, Field


class ActionDetail(BaseModel):
    timestamp: int
    url: str
    title: str
    page_title: str | None = Field(None, alias="pageTitle")
    pageview_position: int | None = Field(None, alias="pageviewPosition")
    time_spent: int = Field(..., alias="timeSpent")


class MatomoDataModel(BaseModel):
    visitor_id: str = Field(..., alias="visitorId")
    site_name: str = Field(..., alias="siteName")
    action_details: ActionDetail = Field(..., alias="actionDetails")
    interactions: int
    language_code: str = Field(..., alias="languageCode")
    browser_name: str = Field(..., alias="browserName")
    browser_version: str = Field(..., alias="browserVersion")
    continent: str
    continent_code: str = Field(..., alias="continentCode")
    country: str
    country_code: str = Field(..., alias="countryCode")
    region: str
    region_code: str = Field(..., alias="regionCode")
    city: str
    latitude: float
    longitude: float
    location: str
    visit_ip: str = Field(..., alias="visitIp")
    referrer_keyword: str | None = Field(None, alias="referrerKeyword")
    referrer_url: str | None = Field(None, alias="referrerUrl")
