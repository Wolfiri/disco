import gevent
import sys
import json

from disco import VERSION
from disco.bot import Plugin


class BasicPlugin(Plugin):
    @Plugin.command('reload')
    def on_reload(self, event):
        self.reload()
        event.msg.reply('Reloaded!')

    @Plugin.listen('MessageCreate')
    def on_message_create(self, msg):
        self.log.info('Message created: {}: {}'.format(msg.author, msg.content))

    @Plugin.command('status', '[component]')
    def on_status_command(self, event, component=None):
        if component == 'state':
            parts = []
            parts.append('Guilds: {}'.format(len(self.state.guilds)))
            parts.append('Channels: {}'.format(len(self.state.channels)))
            parts.append('Users: {}'.format(len(self.state.users)))

            event.msg.reply('State Information: ```\n{}\n```'.format('\n'.join(parts)))
            return

        event.msg.reply('Disco v{} running on Python {}.{}.{}'.format(
            VERSION,
            sys.version_info.major,
            sys.version_info.minor,
            sys.version_info.micro,
        ))

    @Plugin.command('echo', '<content:str...>')
    def on_test_command(self, event, content):
        event.msg.reply(content)

    @Plugin.command('spam', '<count:int> <content:str...>')
    def on_spam_command(self, event, count, content):
        for i in range(count):
            event.msg.reply(content)

    @Plugin.command('invites')
    def on_invites(self, event):
        invites = event.channel.get_invites()
        event.msg.reply('Channel has a total of {} invites'.format(len(invites)))

    @Plugin.command('pins')
    def on_pins(self, event):
        pins = event.channel.get_pins()
        event.msg.reply('Channel has a total of {} pins'.format(len(pins)))

    @Plugin.command('channel stats')
    def on_stats(self, event):
        msg = event.msg.reply('Ok, one moment...')
        invite_count = len(event.channel.get_invites())
        pin_count = len(event.channel.get_pins())
        msg_count = 0

        for msgs in event.channel.messages_iter(bulk=True):
            msg_count += len(msgs)

        msg.edit('{} invites, {} pins, {} messages'.format(invite_count, pin_count, msg_count))

    @Plugin.command('messages stack')
    def on_messages_stack(self, event):
        event.msg.reply('Channels: {}, messages here: ```\n{}\n```'.format(
            len(self.state.messages),
            '\n'.join([str(i.id) for i in self.state.messages[event.channel.id]])
        ))

    @Plugin.command('airhorn')
    def on_airhorn(self, event):
        vs = event.member.get_voice_state()
        if not vs:
            event.msg.reply('You are not connected to voice')
            return

        vc = vs.channel.connect()
        gevent.sleep(1)
        vc.disconnect()

    @Plugin.command('lol')
    def on_lol(self, event):
        event.msg.reply(':^)')
        # event.msg.reply("{}".format(event.channel.can(event.msg.author, Permissions.MANAGE_EMOJIS)))

    @Plugin.command('perms')
    def on_perms(self, event):
        perms = event.channel.get_permissions(event.msg.author)
        event.msg.reply('```json\n{}\n```'.format(
            json.dumps(perms.to_dict(), sort_keys=True, indent=2, separators=(',', ': '))
        ))

    @Plugin.command('tag', '<name:str> [value:str]')
    def on_tag(self, event, name, value=None):
        tags = self.storage.guild.ensure('tags')

        if value:
            tags[name] = value
            event.msg.reply(':ok_hand:')
        else:
            if name in tags:
                return event.msg.reply(tags[name])
            else:
                return event.msg.reply('Unknown tag: `{}`'.format(name))
