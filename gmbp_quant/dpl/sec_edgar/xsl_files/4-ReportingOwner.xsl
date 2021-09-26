<xsl:stylesheet version="2.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" encoding="UTF-8"/>

<xsl:variable name="newline"><xsl:text>
</xsl:text></xsl:variable>
<xsl:variable name="tab"><xsl:text>&#x09;</xsl:text></xsl:variable>

<xsl:template match="/">
  <xsl:text>report_owner_cik&#x09;report_owner_name&#x09;street1&#x09;street2&#x09;city&#x09;state&#x09;zipcode&#x09;state_description&#x09;is_director&#x09;is_officer&#x09;is_ten_percent_owner&#x09;is_other&#x09;officer_title&#x09;other_text</xsl:text>
  <xsl:value-of select="$newline"/>

  <xsl:for-each select="reportingowner">
    <xsl:value-of select="normalize-space(reportingownerid/rptownercik)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(reportingownerid/rptownername)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(reportingowneraddress/rptownerstreet1)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(reportingowneraddress/rptownerstreet2)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(reportingowneraddress/rptownercity)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(reportingowneraddress/rptownerstate)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(reportingowneraddress/rptownerzipcode)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(reportingowneraddress/rptownerstatedescription)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(reportingownerrelationship/isdirector)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(reportingownerrelationship/isofficer)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(reportingownerrelationship/istenpercentowner)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(reportingownerrelationship/isother)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(reportingownerrelationship/officertitle)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(reportingownerrelationship/othertext)"/><xsl:value-of select="$newline"/>
  </xsl:for-each>

</xsl:template>
</xsl:stylesheet>