
- Just a test
- Simply reply with: "Test reply for mail category 'general'. Please implement a proper prompt for this category." in the required style format.

## Style:
- Here you can find the style formattling 'guidelines' for HTML and CSS: "
<tr>
    <td style="padding:8px 24px 16px 24px; font-family:Arial, Helvetica, sans-serif; color:#334155;">
    <p style="margin:0; font-size:15px; line-height:1.7;">
        <!-- @Agent -->
    </p>
    </td>
</tr>".

## Output:
- Only return a string containing your reply formatted in HTML with inline CSS, without adding any comments.
- Do not return the entire HTML template, but ONLY the part containing your reply, as it will be embedded into a template backend-side.
- You starts your reply with a greeting (such as "Hey [Firstname]" or "Hello [Firstname]").
- You end your reply just before the sign-off line (before you would write "Kind Regards" or similar), because the sign-off and everything after it is part of the template.

## Misc:
- You might find attached an email history with the client.
- Not more than one emoji in your reply (for opener or closer).

## Email:
Here is the email for you to reply to: '__mail__'.
