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
    browser_version: str | None = Field(None, alias="browserVersion")
    continent: str | None = Field(None)
    continent_code: str | None = Field(None, alias="continentCode")
    country: str | None = Field(None)
    country_code: str | None = Field(None, alias="countryCode")
    region: str | None = Field(None)
    region_code: str | None = Field(None, alias="regionCode")
    city: str | None = Field(None)
    latitude: float | None = Field(None)
    longitude: float | None = Field(None)
    location: str | None = Field(None)
    visit_ip: str = Field(..., alias="visitIp")
    referrer_keyword: str | None = Field(None, alias="referrerKeyword")
    referrer_url: str | None = Field(None, alias="referrerUrl")
