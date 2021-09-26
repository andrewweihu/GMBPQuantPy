<xsl:stylesheet version="2.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" encoding="UTF-8"/>

<xsl:variable name="newline"><xsl:text>
</xsl:text></xsl:variable>
<xsl:variable name="tab"><xsl:text>&#x09;</xsl:text></xsl:variable>

<xsl:template match="/">
  <xsl:text>security_title&#x09;conversion_or_exercise_price&#x09;exercise_date&#x09;expiration_date&#x09;underlying_security_title&#x09;underlying_security_shares&#x09;direct_or_indirect_ownership&#x09;nature_of_ownership</xsl:text>
  <xsl:value-of select="$newline"/>

  <xsl:for-each select="derivativetable/derivativeholding">
    <xsl:value-of select="normalize-space(securitytitle/value)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(conversionorexerciseprice/value)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(exercisedate/value)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(expirationdate/value)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(underlyingsecurity/underlyingsecuritytitle/value)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(underlyingsecurity/underlyingsecurityshares/value)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(ownershipnature/directorindirectownership/value)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(ownershipnature/natureofownership/value)"/><xsl:value-of select="$newline"/>
  </xsl:for-each>

</xsl:template>
</xsl:stylesheet>