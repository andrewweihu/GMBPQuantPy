<xsl:stylesheet version="2.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" encoding="UTF-8"/>

<xsl:variable name="newline"><xsl:text>
</xsl:text></xsl:variable>
<xsl:variable name="tab"><xsl:text>&#x09;</xsl:text></xsl:variable>

<xsl:template match="/">
  <xsl:text>name&#x09;title_of_class&#x09;cusip&#x09;values&#x09;ssh_prn_amt&#x09;ssh_prn_type&#x09;put_call&#x09;other_manager&#x09;investment_discretion&#x09;voting_authority_sole&#x09;voting_authority_shared&#x09;voting_authority_none</xsl:text>
  <xsl:value-of select="$newline"/>

  <xsl:for-each select="informationtable/infotable">
    <xsl:value-of select="normalize-space(nameofissuer)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(titleofclass)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(cusip)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(value)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(shrsorprnamt/sshprnamt)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(shrsorprnamt/sshprnamttype)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(putcall)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(othermanager)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(investmentdiscretion)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(votingauthority/sole)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(votingauthority/shared)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(votingauthority/none)"/><xsl:value-of select="$newline"/>
  </xsl:for-each>
</xsl:template>

</xsl:stylesheet>